import matplotlib.pyplot as plt
import matplotlib as mlp
import matplotlib.dates as md
from datetime import date
import numpy as np
import yaml
import os
import urllib.request

def create_milestone(dates, labels, as_file=None):
    fig, ax = plt.subplots(figsize=(15, 4), constrained_layout=True)

    min_date = date(np.min(dates).year, np.min(dates).month, max(1, np.min(dates).day-5))
    max_date = date(np.max(dates).year, np.max(dates).month, min(31, np.max(dates).day+5))

    ax.set_ylim(-1, 1.0)
    ax.set_xlim(min_date, max_date)

    # ax.axhline(0, xmin=0.05, xmax=0.95, c='grey', zorder=4)

    ax.scatter(dates, np.zeros(len(dates)), s=120, c='grey', zorder=2)
    ax.scatter(dates, np.zeros(len(dates)), s=30, c='black', zorder=3)

    label_offsets = np.zeros(len(dates))
    label_offsets[::2] = 0.35
    label_offsets[1::2] = -0.7

    for i, (l0, l1, d) in enumerate(zip(labels[0], labels[1], dates)):
        ax.text(d, label_offsets[i], l0, ha='center', fontweight='bold', color='green',fontsize=12)
        ax.text(d, label_offsets[i], l1, ha='center', fontweight='bold', color='black',fontsize=12)

    stems = np.zeros(len(dates))
    stems[::2] = 0.3
    stems[1::2] = -0.3
    markerline, stemline, baseline = ax.stem(dates, stems, use_line_collection=True)
    plt.setp(markerline, marker=',', color='grey')
    plt.setp(stemline, linestyle='--', color='grey')

    #add arrow
    # x0 = md.date2num(date.today())
    # arrow = mlp.patches.FancyArrow(x=x0, y=0.25, dx=-0.0, dy=-0.15, width=3, head_width=10, head_length=0.1, length_includes_head=False, ec='k', fc='k')
    # ax.add_patch(arrow)
    # ax.text(x0, 0.3, 'WE ARE HERE', ha='center', fontweight='bold', color='red',fontsize=12)

    # hide lines around chart
    for spine in ["left", "top", "right", "bottom"]:
        ax.spines[spine].set_visible(True)
        ax.spines[spine].set(bounds=0)
    
    fig.autofmt_xdate()
    # hide tick labels
    ax.set_xticks([])
    ax.set_yticks([])

    if as_file:
        if not os.path.exists(path=f'output'):
            os.mkdir(path=f'output')
        
        plt.savefig(f'output/{as_file}', bbox_inches='tight')

def parse_yaml(url):
    f = urllib.request.urlopen(url=url)
    # with open(files, 'r') as f:
    dat = yaml.safe_load(f)

    for d in dat:
        events = dat[d]['event']
        dates  = [eval(dt) for dt in dat[d]['date']]

        # date_labels = [f'{d:%^b %Y}\n' for l, d in zip (events, dates)]
        date_labels = [f'{d:%^b %Y}\n' for d in dates]
        task_labels = [f'{l.upper()}' for l in events]

        create_milestone(dates=dates, labels=[date_labels, task_labels], as_file=f'{d}.svg')

parse_yaml(url='https://raw.githubusercontent.com/neurodata/neurodata-software/main/doc/milestone.yaml')