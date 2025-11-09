from otree.api import *
import random

doc = """
Spending Game - Supply Chain Resilience with Risk Tasks
"""

class C(BaseConstants):
    NAME_IN_URL = 'otree_nd'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 11
    INITIAL_PROFIT = 10000
    DISRUPTION_COST = 2000
    BASIC_PROBABILITY = 5
    
    # Quiz questions - 8 multiple choice questions
    QUIZ_QUESTIONS_MC = [
        {
            'question': 'How many Rounds do you play in this experiment?',
            'options': [
                {'text': '20 rounds', 'correct': True},
                {'text': '100 rounds'},
                {'text': '120 rounds'}
            ]
        },
        {
            'question': 'How much Gross profit do you earn each round?',
            'options': [
                {'text': '1000 ECU', 'correct': True},
                {'text': '100 ECU'},
                {'text': '200 ECU'}
            ]
        },
        {
            'question': 'What is the Probability of disruptions when your SC resilience spending is zero?',
            'options': [
                {'text': '5%', 'correct': True},
                {'text': '4%'},
                {'text': '4.5%'}
            ]
        },
        {
            'question': 'What is the Impact of disruptions when your SC resilience spending is zero?',
            'options': [
                {'text': '1000 ECU', 'correct': True},
                {'text': '2000 ECU'},
                {'text': '100 ECU'}
            ]
        },
        {
            'question': 'What is your Profit when you spend 20 ECU on SC resilience and no disruption occurs?',
            'options': [
                {'text': '80 ECU', 'correct': True},
                {'text': '-20 ECU'},
                {'text': '-120 ECU'}
            ]
        },
        {
            'question': 'What is the Maximum amount of spending you can make?',
            'options': [
                {'text': '50 ECU', 'correct': True},
                {'text': '2000 ECU'},
                {'text': '100 ECU'}
            ]
        },
        {
            'question': 'What is the Probability of disruptions when your SC resilience spending is 100 ECU?',
            'options': [
                {'text': '5%', 'correct': True},
                {'text': '0%'},
                {'text': '0.5%'}
            ]
        },
        {
            'question': 'What is the Impact of disruptions when your SC resilience spending is 100 ECU?',
            'options': [
                {'text': '2000 ECU', 'correct': True},
                {'text': '100 ECU'},
                {'text': '0 ECU'}
            ]
        }
    ]
    
    # Quiz questions - 2 True/False questions
    QUIZ_QUESTIONS_TF = [
        {
            'question': 'You can decide to spend on SC resilience freely between 0 and 100.',
            'options': [
                {'text': 'True', 'correct': True},
                {'text': 'False'}
            ]
        },
        {
            'question': 'After spending 50 ECU on SC resilience, you can also be at risk of disruptions.',
            'options': [
                {'text': 'True', 'correct': True},
                {'text': 'False'}
            ]
        }
    ]

class Subsession(BaseSubsession):
    pass

class Group(BaseGroup):
    pass

class Player(BasePlayer):
    # Spending game fields
    money_input = models.IntegerField(min=0, max=100, label="", blank=False)
    is_disrupted = models.BooleanField(initial=False)
    cost_of_disruption = models.IntegerField(initial=0)
    total_costs = models.IntegerField(initial=0)
    expected_profit = models.IntegerField(initial=C.INITIAL_PROFIT)
    round_calculated = models.BooleanField(initial=False)
    
    # Quiz fields
    def make_field():
        return models.StringField(
            blank=True,
            choices=[['a', 'a'], ['b', 'b'], ['c', 'c']],
            widget=widgets.RadioSelect
        )
    
    quiz_q1 = make_field()
    quiz_q2 = make_field()
    quiz_q3 = make_field()
    quiz_q4 = make_field()
    quiz_q5 = make_field()
    quiz_attempts = models.IntegerField(initial=0)
    quiz_failed = models.BooleanField(initial=False)
    current_question_indices = models.StringField(initial='')
    
    # Task 1 fields - 10 decisions
    task1_d1 = models.StringField(choices=[['A', 'A'], ['B', 'B']], widget=widgets.RadioSelect)
    task1_d2 = models.StringField(choices=[['A', 'A'], ['B', 'B']], widget=widgets.RadioSelect)
    task1_d3 = models.StringField(choices=[['A', 'A'], ['B', 'B']], widget=widgets.RadioSelect)
    task1_d4 = models.StringField(choices=[['A', 'A'], ['B', 'B']], widget=widgets.RadioSelect)
    task1_d5 = models.StringField(choices=[['A', 'A'], ['B', 'B']], widget=widgets.RadioSelect)
    task1_d6 = models.StringField(choices=[['A', 'A'], ['B', 'B']], widget=widgets.RadioSelect)
    task1_d7 = models.StringField(choices=[['A', 'A'], ['B', 'B']], widget=widgets.RadioSelect)
    task1_d8 = models.StringField(choices=[['A', 'A'], ['B', 'B']], widget=widgets.RadioSelect)
    task1_d9 = models.StringField(choices=[['A', 'A'], ['B', 'B']], widget=widgets.RadioSelect)
    task1_d10 = models.StringField(choices=[['A', 'A'], ['B', 'B']], widget=widgets.RadioSelect)
    task1_selected_decision = models.IntegerField()
    task1_random_number = models.IntegerField()
    task1_payoff = models.IntegerField()
    
    # Task 2 fields - 7 gambles
    task2_g1 = models.StringField(choices=[['accept', 'Accept'], ['reject', 'Reject']], widget=widgets.RadioSelect)
    task2_g2 = models.StringField(choices=[['accept', 'Accept'], ['reject', 'Reject']], widget=widgets.RadioSelect)
    task2_g3 = models.StringField(choices=[['accept', 'Accept'], ['reject', 'Reject']], widget=widgets.RadioSelect)
    task2_g4 = models.StringField(choices=[['accept', 'Accept'], ['reject', 'Reject']], widget=widgets.RadioSelect)
    task2_g5 = models.StringField(choices=[['accept', 'Accept'], ['reject', 'Reject']], widget=widgets.RadioSelect)
    task2_g6 = models.StringField(choices=[['accept', 'Accept'], ['reject', 'Reject']], widget=widgets.RadioSelect)
    task2_g7 = models.StringField(choices=[['accept', 'Accept'], ['reject', 'Reject']], widget=widgets.RadioSelect)
    task2_selected_gamble = models.IntegerField()
    task2_outcome = models.IntegerField()
    task2_payoff = models.IntegerField()

class CombinedResult(ExtraModel):
    player = models.Link(Player)
    spending = models.IntegerField()
    is_disrupted = models.BooleanField()
    cost_of_disruption = models.IntegerField()
    total_costs = models.IntegerField(initial=0)
    expected_profit = models.IntegerField(initial=C.INITIAL_PROFIT)
    task1_d1 = models.StringField()
    task1_d2 = models.StringField()
    task1_d3 = models.StringField()
    task1_d4 = models.StringField()
    task1_d5 = models.StringField()
    task1_d6 = models.StringField()
    task1_d7 = models.StringField()
    task1_d8 = models.StringField()
    task1_d9 = models.StringField()
    task1_d10 = models.StringField()

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
        return player.round_number == 1 and not player.quiz_failed
    
    @staticmethod
    def vars_for_template(player: Player):
        # Select 4 random questions from 8 multiple choice questions
        mc_indices = random.sample(range(len(C.QUIZ_QUESTIONS_MC)), 4)
        
        # Select 1 random question from 2 True/False questions
        tf_index = random.randint(0, len(C.QUIZ_QUESTIONS_TF) - 1)
        
        # Get selected questions and shuffle their options
        selected_questions = []
        option_mappings = []
        
        # Process MC questions
        for i in mc_indices:
            original_q = C.QUIZ_QUESTIONS_MC[i]
            
            # Shuffle options
            shuffled_options = original_q['options'].copy()
            random.shuffle(shuffled_options)
            
            # Convert to dict format for template (a, b, c)
            options_dict = {}
            correct_key = None
            keys = ['a', 'b', 'c']
            
            for j, opt in enumerate(shuffled_options):
                options_dict[keys[j]] = opt['text']
                if opt.get('correct', False):
                    correct_key = keys[j]
            
            selected_questions.append({
                'question': original_q['question'],
                'options': options_dict,
            })
            
            option_mappings.append(correct_key)
        
        # Process TF question
        original_tf = C.QUIZ_QUESTIONS_TF[tf_index]
        
        # Shuffle True/False
        shuffled_tf = original_tf['options'].copy()
        random.shuffle(shuffled_tf)
        
        tf_options_dict = {}
        tf_correct_key = None
        
        for j, opt in enumerate(shuffled_tf):
            tf_options_dict[['a', 'b'][j]] = opt['text']
            if opt.get('correct', False):
                tf_correct_key = ['a', 'b'][j]
        
        selected_questions.append({
            'question': original_tf['question'],
            'options': tf_options_dict,
        })
        
        option_mappings.append(tf_correct_key)
        
        # Store indices and correct answer mappings for validation
        indices_str = ','.join(map(str, mc_indices)) + f',TF{tf_index}'
        mappings_str = ','.join(option_mappings)
        player.current_question_indices = indices_str + '|' + mappings_str
        
        return dict(
            questions=selected_questions,
            attempt_number=player.quiz_attempts + 1,
        )
    
    @staticmethod
    def error_message(player: Player, values):
        # Check if all questions are answered
        unanswered = []
        for i in range(1, 6):
            field_name = f'quiz_q{i}'
            if not values.get(field_name):
                unanswered.append(str(i))
        
        if unanswered:
            return "Please answer all questions before submitting"
        
        # Parse current question indices and mappings
        parts = player.current_question_indices.split('|')
        indices_str = parts[0]
        mappings_str = parts[1]
        
        correct_keys = mappings_str.split(',')
        
        # Check answers
        errors = []
        
        # Check all 5 questions using the stored correct keys
        for i in range(1, 6):
            field_name = f'quiz_q{i}'
            if values[field_name] != correct_keys[i-1]:
                errors.append(str(i))
        
        if errors:
            player.quiz_attempts += 1
            return f"Some answers are incorrect. Please try again. (Attempt {player.quiz_attempts + 1})"

class Unfortunately(Page):
    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == 1 and player.quiz_failed

class GamePage(Page):
    form_model = 'player'
    form_fields = ['money_input']
    
    @staticmethod
    def is_displayed(player: Player):
        if player.round_number == 1:
            return not player.quiz_failed
        return True
    
    @staticmethod
    def vars_for_template(player: Player):
        all_players = player.in_all_rounds()
        results = []
        for p in all_players[:player.round_number]:
            player_results = CombinedResult.filter(player=p)
            for r in player_results:
                r.round_total_costs = r.spending + r.cost_of_disruption
                r.round_profit = 100 - r.spending - r.cost_of_disruption
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
            accumulative_costs = sum(r.spending + r.cost_of_disruption for r in results)
        
        accumulative_profit = 0
        if results:
            accumulative_profit = sum(100 - r.spending - r.cost_of_disruption for r in results)
        
        current_profit = last_result.expected_profit if last_result else C.INITIAL_PROFIT
        
        game_completed = (player.round_number == C.NUM_ROUNDS and 
                         len(CombinedResult.filter(player=player)) > 0)
        
        final_stats = None
        if game_completed:
            total_spending = sum(r.spending for r in results)
            total_disruption_cost = sum(r.cost_of_disruption for r in results)
            final_profit = results[0].expected_profit if results else C.INITIAL_PROFIT
            
            final_stats = {
                'total_spending': total_spending,
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
            spending = data['spending']
            
            if spending < 0 or spending > 100:
                return {'status': 'error', 'message': 'spending must be between 0 and 100'}
            
            player.money_input = spending
            
            disruption_probability = C.BASIC_PROBABILITY * (1 - spending / 100)
            disruption_probability = max(0, disruption_probability)
            
            disruption_impact = C.DISRUPTION_COST * (1 - spending / 100)
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
                
                player.expected_profit = prev_expected_profit - spending - player.cost_of_disruption
                player.total_costs = prev_total_costs + spending + player.cost_of_disruption
            else:
                player.expected_profit = C.INITIAL_PROFIT - spending - player.cost_of_disruption
                player.total_costs = spending + player.cost_of_disruption
            
            existing_results = CombinedResult.filter(player=player)
            for result in existing_results:
                result.delete()
            
            CombinedResult.create(
                player=player,
                spending=spending,
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
                    'spending': spending,
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
            spending = player.money_input
            
            disruption_probability = C.BASIC_PROBABILITY * (1 - spending / 100)
            disruption_probability = max(0, disruption_probability)
            
            disruption_impact = C.DISRUPTION_COST * (1 - spending / 100)
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
                
                player.expected_profit = prev_expected_profit - spending - player.cost_of_disruption
                player.total_costs = prev_total_costs + spending + player.cost_of_disruption
            else:
                player.expected_profit = C.INITIAL_PROFIT - spending - player.cost_of_disruption
                player.total_costs = spending + player.cost_of_disruption
            
            existing_results = CombinedResult.filter(player=player)
            for result in existing_results:
                result.delete()
            
            CombinedResult.create(
                player=player,
                spending=spending,
                is_disrupted=player.is_disrupted,
                cost_of_disruption=player.cost_of_disruption,
                total_costs=player.total_costs,
                expected_profit=player.expected_profit,
            )

class Results(Page):
    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == C.NUM_ROUNDS and not player.in_round(1).quiz_failed
    
    @staticmethod
    def vars_for_template(player: Player):
        all_players = player.in_all_rounds()
        all_results = []
        for p in all_players:
            player_results = CombinedResult.filter(player=p)
            all_results.extend(player_results)

        all_results = sorted(all_results, key=lambda x: x.player.round_number)
        
        total_spending = sum(r.spending for r in all_results)
        total_disruption_cost = sum(r.cost_of_disruption for r in all_results)
        final_profit = all_results[-1].expected_profit if all_results else C.INITIAL_PROFIT
        average_spending = total_spending // C.NUM_ROUNDS if all_results else 0
        num_disruptions = sum(1 for r in all_results if r.is_disrupted)
        
        show_up_fee = 3
        conversion_rate = 1 / 1500
        
        performance_payment = final_profit * conversion_rate
        performance_payment = round(performance_payment, 1)
        
        total_payment = show_up_fee + performance_payment
        total_payment = round(total_payment, 1)
        
        player.participant.payoff = total_payment
        
        return dict(
            all_results=all_results,
            total_results=len(all_results),
            num_disruptions=num_disruptions,
            total_disruption_cost=total_disruption_cost,
            total_spending=total_spending,
            final_profit=final_profit,
            initial_profit=C.INITIAL_PROFIT,
            average_spending=average_spending,
            show_up_fee=show_up_fee,
            performance_payment=performance_payment,
            total_payment=total_payment,
        )

class Task1(Page):
    form_model = 'player'
    form_fields = ['task1_d1', 'task1_d2', 'task1_d3', 'task1_d4', 'task1_d5',
                   'task1_d6', 'task1_d7', 'task1_d8', 'task1_d9', 'task1_d10']
    
    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == C.NUM_ROUNDS and not player.in_round(1).quiz_failed
    
    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        player.task1_selected_decision = random.randint(1, 10)
        player.task1_random_number = random.randint(1, 10)
        
        decision_field = f'task1_d{player.task1_selected_decision}'
        choice = getattr(player, decision_field)
        
        # Updated payoffs to match new ECU values: 2000, 1600, 3850, 100
        decisions = {
            1: {'A': {1: 2000, 'other': 1600}, 'B': {1: 3850, 'other': 100}},
            2: {'A': {1: 2000, 2: 2000, 'other': 1600}, 'B': {1: 3850, 2: 3850, 'other': 100}},
            3: {'A': {1: 2000, 2: 2000, 3: 2000, 'other': 1600}, 'B': {1: 3850, 2: 3850, 3: 3850, 'other': 100}},
            4: {'A': {1: 2000, 2: 2000, 3: 2000, 4: 2000, 'other': 1600}, 'B': {1: 3850, 2: 3850, 3: 3850, 4: 3850, 'other': 100}},
            5: {'A': {1: 2000, 2: 2000, 3: 2000, 4: 2000, 5: 2000, 'other': 1600}, 'B': {1: 3850, 2: 3850, 3: 3850, 4: 3850, 5: 3850, 'other': 100}},
            6: {'A': {1: 2000, 2: 2000, 3: 2000, 4: 2000, 5: 2000, 6: 2000, 'other': 1600}, 'B': {1: 3850, 2: 3850, 3: 3850, 4: 3850, 5: 3850, 6: 3850, 'other': 100}},
            7: {'A': {1: 2000, 2: 2000, 3: 2000, 4: 2000, 5: 2000, 6: 2000, 7: 2000, 'other': 1600}, 'B': {1: 3850, 2: 3850, 3: 3850, 4: 3850, 5: 3850, 6: 3850, 7: 3850, 'other': 100}},
            8: {'A': {1: 2000, 2: 2000, 3: 2000, 4: 2000, 5: 2000, 6: 2000, 7: 2000, 8: 2000, 'other': 1600}, 'B': {1: 3850, 2: 3850, 3: 3850, 4: 3850, 5: 3850, 6: 3850, 7: 3850, 8: 3850, 'other': 100}},
            9: {'A': {1: 2000, 2: 2000, 3: 2000, 4: 2000, 5: 2000, 6: 2000, 7: 2000, 8: 2000, 9: 2000, 'other': 1600}, 'B': {1: 3850, 2: 3850, 3: 3850, 4: 3850, 5: 3850, 6: 3850, 7: 3850, 8: 3850, 9: 3850, 'other': 100}},
            10: {'A': {1: 2000, 2: 2000, 3: 2000, 4: 2000, 5: 2000, 6: 2000, 7: 2000, 8: 2000, 9: 2000, 10: 2000, 'other': 1600}, 'B': {1: 3850, 2: 3850, 3: 3850, 4: 3850, 5: 3850, 6: 3850, 7: 3850, 8: 3850, 9: 3850, 10: 3850, 'other': 100}},
        }
        
        decision_payoffs = decisions[player.task1_selected_decision][choice]
        if player.task1_random_number in decision_payoffs:
            player.task1_payoff = decision_payoffs[player.task1_random_number]
        else:
            player.task1_payoff = decision_payoffs['other']

class Task2(Page):
    form_model = 'player'
    form_fields = ['task2_g1', 'task2_g2', 'task2_g3', 'task2_g4', 'task2_g5', 'task2_g6']
    
    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == C.NUM_ROUNDS and not player.in_round(1).quiz_failed
    
    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        player.task2_selected_gamble = random.randint(1, 6)
        
        gamble_field = f'task2_g{player.task2_selected_gamble}'
        choice = getattr(player, gamble_field)
        
        gambles = {
            1: (-2000, 6000),
            2: (-3000, 6000),
            3: (-4000, 6000),
            4: (-5000, 6000),
            5: (-6000, 6000),
            6: (-7000, 6000),
        }
        
        if choice == 'reject':
            player.task2_payoff = 0
            player.task2_outcome = 0
        else:
            outcome = random.choice([0, 1])
            player.task2_outcome = outcome
            
            if outcome == 0:
                player.task2_payoff = gambles[player.task2_selected_gamble][0]
            else:
                player.task2_payoff = gambles[player.task2_selected_gamble][1]

class FinalResults(Page):
    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == C.NUM_ROUNDS and not player.in_round(1).quiz_failed
    
    @staticmethod
    def vars_for_template(player: Player):
        all_players = player.in_all_rounds()
        all_results = []
        for p in all_players:
            player_results = CombinedResult.filter(player=p)
            all_results.extend(player_results)

        all_results = sorted(all_results, key=lambda x: x.player.round_number)
        
        total_spending = sum(r.spending for r in all_results)
        total_disruption_cost = sum(r.cost_of_disruption for r in all_results)
        final_profit = all_results[-1].expected_profit if all_results else C.INITIAL_PROFIT
        
        show_up_fee = 3
        conversion_rate = 1 / 1500
        performance_payment = final_profit * conversion_rate
        performance_payment = round(performance_payment, 1)
        spending_game_payment = show_up_fee + performance_payment
        
        # Calculate tasks payment (convert ECU to dollars)
        task1_payment = round(player.task1_payoff * conversion_rate, 1)
        task2_payment = round(player.task2_payoff * conversion_rate, 1)
        tasks_total_payment = round(task1_payment + task2_payment, 1)
        
        # Total payment
        total_payment = round(spending_game_payment + tasks_total_payment, 1)
        player.participant.payoff = total_payment
        
        return dict(
            # Spending game
            final_profit=final_profit,
            initial_profit=C.INITIAL_PROFIT,
            show_up_fee=show_up_fee,
            performance_payment=performance_payment,
            spending_game_payment=spending_game_payment,
            
            # Task 1
            task1_selected_decision=player.task1_selected_decision,
            task1_random_number=player.task1_random_number,
            task1_choice=getattr(player, f'task1_d{player.task1_selected_decision}'),
            task1_payoff=player.task1_payoff,
            task1_payment=task1_payment,
            
            # Task 2
            task2_selected_gamble=player.task2_selected_gamble,
            task2_choice=getattr(player, f'task2_g{player.task2_selected_gamble}'),
            task2_outcome=player.task2_outcome,
            task2_payoff=player.task2_payoff,
            task2_payment=task2_payment,
            
            # Totals
            tasks_total_payment=tasks_total_payment,
            total_payment=total_payment,
        )

def custom_export_1(players):
    players = sorted(players, key=lambda p: (p.id_in_group, p.round_number))

    yield [
        'player_id',
        'round_number',
        'spending',
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
                r.spending,
                1 if r.is_disrupted else 0,
                r.cost_of_disruption,
                r.total_costs,
                r.expected_profit
            ]

def custom_export_2(players):
    players = sorted(players, key=lambda p: (p.id_in_group))

    yield [
        'player_id','task1_d1', 'task1_d2', 'task1_d3', 'task1_d4', 'task1_d5',
        'task1_d6', 'task1_d7', 'task1_d8', 'task1_d9', 'task1_d10',
        'task1_selected_decision', 'task1_random_number', 'task1_payoff',
        'task2_g1', 'task2_g2', 'task2_g3', 'task2_g4', 'task2_g5', 'task2_g6',
        'task2_selected_gamble', 'task2_outcome', 'task2_payoff',
    ]

    for p in players:
        if p.task1_selected_decision is not None:
            yield [
                p.id_in_group,
                p.task1_d1,
                p.task1_d2,
                p.task1_d3,
                p.task1_d4,
                p.task1_d5,
                p.task1_d6,
                p.task1_d7,
                p.task1_d8,
                p.task1_d9,
                p.task1_d10,
                p.task1_selected_decision,
                p.task1_random_number,
                p.task1_payoff,
                p.task2_g1,
                p.task2_g2,
                p.task2_g3,
                p.task2_g4,
                p.task2_g5,
                p.task2_g6,
                p.task2_selected_gamble,
                p.task2_outcome,
                p.task2_payoff,
            ]

page_sequence = [LandingPage, QuizPage, Unfortunately, GamePage, Results, Task1, Task2, FinalResults]