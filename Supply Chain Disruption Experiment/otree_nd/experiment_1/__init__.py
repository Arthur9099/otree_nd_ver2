from otree.api import *
import random

doc = """
Investment Game - Supply Chain Resilience
"""

class C(BaseConstants):
    NAME_IN_URL = 'otree_nd'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 11
    INITIAL_PROFIT = 10000  # C₀
    DISRUPTION_COST = 2000  # C_I (base disruption cost)
    BASIC_PROBABILITY = 5   # p₀ (base probability in %)
    
    # Quiz questions and answers
    QUIZ_QUESTIONS = [
        {
            'question': 'Câu hỏi 1: (Đáp án a)',
            'options': {
                'a': 'Nội dung câu a',
                'b': 'Nội dung câu b',
                'c': 'Nội dung câu c',
                'd': 'Nội dung câu d'
            },
            'correct': 'a'
        },
        {
            'question': 'Câu hỏi 2: (Đáp án b)',
            'options': {
                'a': 'Nội dung câu a',
                'b': 'Nội dung câu b',
                'c': 'Nội dung câu c',
                'd': 'Nội dung câu d'
            },
            'correct': 'b'
        },
        {
            'question': 'Câu hỏi 3: (Đáp án c)',
            'options': {
                'a': 'Nội dung câu a',
                'b': 'Nội dung câu b',
                'c': 'Nội dung câu c',
                'd': 'Nội dung câu d'
            },
            'correct': 'c'
        },
        {
            'question': 'Câu hỏi 4: (Đáp án d)',
            'options': {
                'a': 'Nội dung câu a',
                'b': 'Nội dung câu b',
                'c': 'Nội dung câu c',
                'd': 'Nội dung câu d'
            },
            'correct': 'd'
        },
        {
            'question': 'Câu hỏi 5: (Đáp án a)',
            'options': {
                'a': 'Nội dung câu a',
                'b': 'Nội dung câu b',
                'c': 'Nội dung câu c',
                'd': 'Nội dung câu d'
            },
            'correct': 'a'
        }
    ]

class Subsession(BaseSubsession):
    pass

class Group(BaseGroup):
    pass

class Player(BasePlayer):
    money_input = models.IntegerField(
        min=0,
        max=100,
        label="",
        blank=False,
    )
    is_disrupted = models.BooleanField(
        initial=False
    )
    cost_of_disruption = models.IntegerField(
        initial=0,
    )
    total_costs = models.IntegerField(
        initial=0,
    )
    expected_profit = models.IntegerField(
        initial=C.INITIAL_PROFIT,
    )
    round_calculated = models.BooleanField(initial=False)
    
    # Quiz fields - choices generated dynamically from QUIZ_QUESTIONS
    def make_field(question_data):
        choices = [[key, f"{key}) {value}"] for key, value in question_data['options'].items()]
        return models.StringField(
            blank=True,
            choices=choices,
            widget=widgets.RadioSelect
        )
    
    quiz_q1 = make_field(C.QUIZ_QUESTIONS[0])
    quiz_q2 = make_field(C.QUIZ_QUESTIONS[1])
    quiz_q3 = make_field(C.QUIZ_QUESTIONS[2])
    quiz_q4 = make_field(C.QUIZ_QUESTIONS[3])
    quiz_q5 = make_field(C.QUIZ_QUESTIONS[4])
    
    quiz_attempts = models.IntegerField(initial=0)

class CombinedResult(ExtraModel):
    player = models.Link(Player)
    investment = models.IntegerField()
    is_disrupted = models.BooleanField()
    cost_of_disruption = models.IntegerField()
    total_costs = models.IntegerField(initial=0)
    expected_profit = models.IntegerField(initial=C.INITIAL_PROFIT)

# PAGES
class LandingPage(Page):
    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == 1

class QuizPage(Page):
    form_model = 'player'
    form_fields = ['quiz_q1', 'quiz_q2', 'quiz_q3', 'quiz_q4', 'quiz_q5']
    
    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == 1
    
    @staticmethod
    def vars_for_template(player: Player):
        return dict(
            questions=C.QUIZ_QUESTIONS,
            attempt_number=player.quiz_attempts + 1
        )
    
    @staticmethod
    def error_message(player: Player, values):
        player.quiz_attempts += 1
        
        errors = []
        for i, q in enumerate(C.QUIZ_QUESTIONS, 1):
            field_name = f'quiz_q{i}'
            if values[field_name] != q['correct']:
                errors.append(f"Question {i}")
        
        if errors:
            return f"Please review your answers. Incorrect: {', '.join(errors)}"

class GamePage(Page):
    form_model = 'player'
    form_fields = ['money_input']
    
    @staticmethod
    def vars_for_template(player: Player):
        all_players = player.in_all_rounds()
        results = []
        for p in all_players[:player.round_number]:
            player_results = CombinedResult.filter(player=p)
            for r in player_results:
                r.round_total_costs = r.investment + r.cost_of_disruption
                r.round_profit = 100 - r.investment - r.cost_of_disruption
            results.extend(player_results)
        
        results = sorted(results, key=lambda x: x.player.round_number, reverse=True)
        
        current_round_result = None
        if player.round_calculated:
            current_results = CombinedResult.filter(player=player)
            if current_results:
                current_round_result = current_results[0]
        
        last_result = results[0] if results else None
        
        accumulative_costs = 0
        if results:
            accumulative_costs = sum(r.investment + r.cost_of_disruption for r in results)
        
        accumulative_profit = 0
        if results:
            accumulative_profit = sum(100 - r.investment - r.cost_of_disruption for r in results)
        
        current_profit = last_result.expected_profit if last_result else C.INITIAL_PROFIT
        
        game_completed = (player.round_number == C.NUM_ROUNDS and 
                         len(CombinedResult.filter(player=player)) > 0)
        
        final_stats = None
        if game_completed:
            total_investment = sum(r.investment for r in results)
            total_disruption_cost = sum(r.cost_of_disruption for r in results)
            final_profit = results[0].expected_profit if results else C.INITIAL_PROFIT
            
            final_stats = {
                'total_investment': total_investment,
                'total_disruption_cost': total_disruption_cost,
                'final_profit': final_profit,
                'initial_profit': C.INITIAL_PROFIT,
                'all_results': results,
            }
        
        return dict(
            combined_result=results,
            current_round_result=current_round_result,
            last_result=last_result,
            accumulative_costs=accumulative_costs,
            accumulative_profit=accumulative_profit,
            initial_profit=C.INITIAL_PROFIT,
            current_profit=current_profit,
            is_final_round=player.round_number == C.NUM_ROUNDS,
            game_completed=game_completed,
            final_stats=final_stats,
            round_calculated=player.round_calculated,
        )
    
    @staticmethod
    def live_method(player: Player, data):
        if data['action'] == 'calculate_result':
            investment = data['investment']
            
            if investment < 0 or investment > 100:
                return {'status': 'error', 'message': 'Investment must be between 0 and 100'}
            
            player.money_input = investment
            
            disruption_probability = C.BASIC_PROBABILITY * (1 - investment / 100)
            disruption_probability = max(0, disruption_probability)
            
            disruption_impact = C.DISRUPTION_COST * (1 - investment / 100)
            disruption_impact = max(0, int(disruption_impact))
            
            random_number = random.uniform(0, 100)
            
            if random_number < disruption_probability:
                player.is_disrupted = True
                player.cost_of_disruption = disruption_impact
            else:
                player.is_disrupted = False
                player.cost_of_disruption = 0
            
            if player.round_number > 1:
                prev_player = player.in_round(player.round_number - 1)
                prev_results = CombinedResult.filter(player=prev_player)
                if prev_results:
                    prev_expected_profit = prev_results[0].expected_profit
                    prev_total_costs = prev_results[0].total_costs
                else:
                    prev_expected_profit = C.INITIAL_PROFIT
                    prev_total_costs = 0
                
                player.expected_profit = prev_expected_profit - investment - player.cost_of_disruption
                player.total_costs = prev_total_costs + investment + player.cost_of_disruption
            else:
                player.expected_profit = C.INITIAL_PROFIT - investment - player.cost_of_disruption
                player.total_costs = investment + player.cost_of_disruption
            
            existing_results = CombinedResult.filter(player=player)
            for result in existing_results:
                result.delete()
            
            CombinedResult.create(
                player=player,
                investment=investment,
                is_disrupted=player.is_disrupted,
                cost_of_disruption=player.cost_of_disruption,
                total_costs=player.total_costs,
                expected_profit=player.expected_profit,
            )
            
            player.round_calculated = True
            
            return {
                'status': 'success',
                'result': {
                    'round': player.round_number,
                    'investment': investment,
                    'is_disrupted': player.is_disrupted,
                    'disruption_probability': round(disruption_probability, 2),
                    'disruption_impact_if_occurs': disruption_impact,
                    'cost_of_disruption': player.cost_of_disruption,
                    'total_costs': player.total_costs,
                    'expected_profit': player.expected_profit,
                }
            }
        
        elif data['action'] == 'next_round':
            player.round_calculated = False
            return {'status': 'next_round'}
    
    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        if not player.round_calculated and player.money_input is not None:
            investment = player.money_input
            
            disruption_probability = C.BASIC_PROBABILITY * (1 - investment / 100)
            disruption_probability = max(0, disruption_probability)
            
            disruption_impact = C.DISRUPTION_COST * (1 - investment / 100)
            disruption_impact = max(0, int(disruption_impact))
            
            random_number = random.uniform(0, 100)
            
            if random_number < disruption_probability:
                player.is_disrupted = True
                player.cost_of_disruption = disruption_impact
            else:
                player.is_disrupted = False
                player.cost_of_disruption = 0
            
            if player.round_number > 1:
                prev_player = player.in_round(player.round_number - 1)
                prev_results = CombinedResult.filter(player=prev_player)
                if prev_results:
                    prev_expected_profit = prev_results[0].expected_profit
                    prev_total_costs = prev_results[0].total_costs
                else:
                    prev_expected_profit = C.INITIAL_PROFIT
                    prev_total_costs = 0
                
                player.expected_profit = prev_expected_profit - investment - player.cost_of_disruption
                player.total_costs = prev_total_costs + investment + player.cost_of_disruption
            else:
                player.expected_profit = C.INITIAL_PROFIT - investment - player.cost_of_disruption
                player.total_costs = investment + player.cost_of_disruption
            
            existing_results = CombinedResult.filter(player=player)
            for result in existing_results:
                result.delete()
            
            CombinedResult.create(
                player=player,
                investment=investment,
                is_disrupted=player.is_disrupted,
                cost_of_disruption=player.cost_of_disruption,
                total_costs=player.total_costs,
                expected_profit=player.expected_profit,
            )


class Results(Page):
    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == C.NUM_ROUNDS
    
    @staticmethod
    def vars_for_template(player: Player):
        all_players = player.in_all_rounds()
        all_results = []
        for p in all_players:
            player_results = CombinedResult.filter(player=p)
            all_results.extend(player_results)

        all_results = sorted(all_results, key=lambda x: x.player.round_number)
        
        total_investment = sum(r.investment for r in all_results)
        total_disruption_cost = sum(r.cost_of_disruption for r in all_results)
        final_profit = all_results[-1].expected_profit if all_results else C.INITIAL_PROFIT
        average_investment = total_investment // C.NUM_ROUNDS if all_results else 0
        num_disruptions = sum(1 for r in all_results if r.is_disrupted)
        profit_change = final_profit - C.INITIAL_PROFIT
        
        show_up_fee = 3
        conversion_rate = 1 / 1000
        
        profit_change = final_profit - C.INITIAL_PROFIT
        performance_payment = max(0, profit_change * conversion_rate)
        performance_payment = round(performance_payment, 2)
        
        total_payment = show_up_fee + performance_payment
        total_payment = round(total_payment, 2)
        
        player.participant.payoff = total_payment
        
        return dict(
            all_results=all_results,
            total_results=len(all_results),
            num_disruptions=num_disruptions,
            total_disruption_cost=total_disruption_cost,
            total_investment=total_investment,
            final_profit=final_profit,
            initial_profit=C.INITIAL_PROFIT,
            average_investment=average_investment,
            profit_change=profit_change,
            show_up_fee=show_up_fee,
            performance_payment=performance_payment,
            total_payment=total_payment,
        )


def custom_export(players):
    players = sorted(players, key=lambda p: (p.id_in_group, p.round_number))

    yield [
        'player_id',
        'round_number',
        'investment',
        'is_disrupted',
        'cost_of_disruption',
        'total_costs',
        'expected_profit',
    ]

    for p in players:
        results = CombinedResult.filter(player=p)
        for r in results:
            yield [
                p.id_in_group,
                p.round_number,
                r.investment,
                1 if r.is_disrupted else 0,
                r.cost_of_disruption,
                r.total_costs,
                r.expected_profit,
            ]

    
page_sequence = [LandingPage, QuizPage, GamePage, Results]