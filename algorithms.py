def calculate_divergence(task):
    completions = task['completions']
    trials = task['trials']
    return ((trials - completions) / trials) * 100


def get_overall_divergence(user_tasks) -> float:
    trials = sum([task['trials'] for task in user_tasks])
    completions = sum([task['completions'] for task in user_tasks])
    if trials == 0:
        return 0
    else:
        return ((trials - completions) / trials) * 100
