from bump_chart import plot_bump_chart
import pandas as pd
from collections import OrderedDict

data = OrderedDict((
    ('Aggressive',   [60, 50, 40, 30, 20, 10, 00, 00, 00, 00, 00, 00]),
    ('Conservative', [60, 40, 20, 10, 00, 50, 30, 00, 00, 00, 00, 00]),
    ('Marco',        [60, 50, 00, 00, 00, 30, 00, 40, 20, 10, 00, 00]),
    ('William',      [60, 50, 00, 00, 00, 40, 00, 20, 00, 00, 30, 10])
))
goals = [
    '3, 1, 3, None',
    '3, 2, 3, None',
    'None, 3, 3, None',
    'None, 2, 3, None',
    'None, 1, 3, None',
    '3, 1, None, 3',
    'None, 1, None, 4',
    '3, 1, 2, None',
    '3, 3, 3, None',
    '3, 2, 2, None',
    '3, 1, 3, 3',
    '2, 1, 3, None'
]

colors = [
    'green',
    'darkred',
    'indigo',
    'darkgoldenrod',
    'black',
    'mediumblue',
    'darkorange',
    'lightseagreen',
    'deepskyblue',
    'red',
    'magenta',
    'dimgrey'
]

data = pd.DataFrame(data)
data['goals'] = pd.Series(goals)
data = data.set_index('goals')

plot_bump_chart(
    data,
    title="Ranking of goals",
    colors=OrderedDict((g, c) for g, c in zip(goals, colors)),
    savename=['bumps.png', 'bumps.pdf'],
    dpi=300
)
