#!/usr/bin/env python3

import os.path as osp
import sys
sys.path.append('..')

import matplotlib as mpl
import numpy as np
import pandas as pd
import seaborn as sns
from matplotlib import pyplot as plt

import common as c
import graphs
import target_stats as t

strange_const = 3

full = True
suffix = '-full' if full else ""

n_cols = 1
n_rows = 4

gm = graphs.GraphMaker(
        fig_size=(7,7.2),
        multi_ax=True,
        legend_loc='best',
        with_xtick_label=False,
        frameon=False,
        nrows=n_rows,
        ncols=n_cols,
        sharex='all')

with open('./bench_order.txt') as f:
    index_order = [l.strip() for l in f]

def spec_on_xbar4():
    global gm
    gm.set_cur_ax(gm.ax[0])
    plt.sca(gm.cur_ax)

    baseline_stat_dirs = {
            'Xbar4': c.env.data('xbar4-rand'),
            # 'Omega16-OPR': c.env.data('omega-rand'),
            }
    stat_dirs = {
            # 'Xbar4*2-SpecSB': c.env.data('dedi-xbar4-rand-hint'),
            'Xbar4-SpecSB': c.env.data('xbar4-rand-hint'),
            # 'Omega16-OPR-SpecSB': c.env.data('omega-rand-hint'),
            # 'Xbar16-OPR': c.env.data('xbar-rand'),
            }
    stats = ['queueingD', 'ssrD']
    for k in baseline_stat_dirs:
        baseline_stat_dirs[k] += suffix
    for k in stat_dirs:
        stat_dirs[k] += suffix

    baselines_ordered = [x for x in baseline_stat_dirs]
    configs_ordered = [x for x in stat_dirs]

    benchmarks = [*c.get_spec2017_int(), *c.get_spec2017_fp()]

    points = []
    for b in benchmarks:
        for i in range(0, 3):
            points.append(f'{b}_{i}')

    num_points, num_configs = 0, len(stat_dirs)

    data_all = []
    for stat in stats:
        baseline_stat_dir = baseline_stat_dirs[baselines_ordered[0]]
        stat_files = [osp.join(baseline_stat_dir, point, 'stats.txt') for point in points]
        matrix = {}
        for point, stat_file in zip(points, stat_files):
            d = c.get_stats(stat_file, t.breakdown_targets, re_targets=True)
            matrix[point] = d
        baseline_df = pd.DataFrame.from_dict(matrix, orient='index')
        baseline_df = baseline_df.reindex(index_order)

        if num_points == 0:
            num_points = len(baseline_df)

        baseline_df.loc['mean'] = baseline_df.iloc[-1]
        baseline_df.loc['mean'][stat] = np.mean(baseline_df[stat])

        data = np.concatenate([baseline_df[stat].values[:-1], [np.NaN],
            baseline_df[stat].values[-1:]])
        print(data.shape)
        data_all.append(data)

    legends = [
            'Xbar4 Queuing', 'Xbar4 SSR',
            'Xbar4-SpecSB Queuing', 'Xbar4-SpecSB SSR',
            ]

    for nc, stat in enumerate(stats):
        stat_dir = stat_dirs[configs_ordered[0]]
        stat_dir = osp.expanduser(stat_dir)
        stat_files = [osp.join(stat_dir, point, 'stats.txt') for point in points]

        matrix = {}
        for point, stat_file in zip(points, stat_files):
            d = c.get_stats(stat_file, t.breakdown_targets, re_targets=True)
            d['mean'] = np.mean(list(d.values()))
            matrix[point] = d

        df = pd.DataFrame.from_dict(matrix, orient='index')
        df = df.reindex(index_order)

        df.loc['mean'] = df.iloc[-1]
        df.loc['mean'][stat] = np.mean(df[stat])
        data = np.concatenate([df[stat].values[:-1],
            [np.NaN],df[stat].values[-1:]])
        print(data/data_all[nc])
        print(data.shape)
        data_all.append(data)


    num_points += 2
    data_all = np.array(data_all)
    print(data_all.shape)

    benchmarks_ordered = []
    for point in df.index:
        if point.endswith('_0'):
            benchmarks_ordered.append(point.split('_')[0])

    xticklabels = [''] * num_points
    print(len(xticklabels))
    for i, benchmark in enumerate(benchmarks_ordered + ['mean']):
        xticklabels[i*strange_const + 1] = benchmark

    print(num_points, num_configs)
    legends = [
            'Xbar4 Queueing', 'Xbar4 SSR',
            'Xbar4-SpecSB Queueing', 'Xbar4-SpecSB SSR',
            ]
    fig, ax = gm.simple_bar_graph(data_all, xticklabels, legends,
            ylabel='Cycles',
            xlim=(-0.5, num_points-0.5),
            ylim=(0,1.22e9),
            title='(a) Effect of Speculative SB/ARF on baseline architecutre',
            colors=['red', 'gray', 'green', 'blue'],
            markers=['+', 7, 'x', 6],
            dont_legend=True,
            )

    ax.legend(
            legends,
            loc = 'upper left',
            # bbox_to_anchor=(0, 0),
            ncol=2,
            fancybox=True,
            framealpha=0.5,
            fontsize=13,
            )

def spec_on_omega():
    global gm
    gm.set_cur_ax(gm.ax[1])
    plt.sca(gm.cur_ax)

    baseline_stat_dirs = {
            # 'Xbar4': c.env.data('xbar4-rand'),
            'Omega16-OPR': c.env.data('omega-rand'),
            }
    stat_dirs = {
            # 'Xbar4*2-SpecSB': c.env.data('dedi-xbar4-rand-hint'),
            # 'Xbar4-SpecSB': c.env.data('xbar4-rand-hint'),
            'Omega16-OPR-SpecSB': c.env.data('omega-rand-hint'),
            # 'Xbar16-OPR': c.env.data('xbar-rand'),
            }
    stats = ['queueingD', 'ssrD']
    for k in baseline_stat_dirs:
        baseline_stat_dirs[k] += suffix
    for k in stat_dirs:
        stat_dirs[k] += suffix

    baselines_ordered = [x for x in baseline_stat_dirs]
    configs_ordered = [x for x in stat_dirs]

    benchmarks = [*c.get_spec2017_int(), *c.get_spec2017_fp()]

    points = []
    for b in benchmarks:
        for i in range(0, 3):
            points.append(f'{b}_{i}')

    num_points, num_configs = 0, len(stat_dirs)

    data_all = []

    for stat in stats:
        baseline_stat_dir = baseline_stat_dirs[baselines_ordered[0]]
        stat_files = [osp.join(baseline_stat_dir, point, 'stats.txt') for point in points]
        matrix = {}
        for point, stat_file in zip(points, stat_files):
            d = c.get_stats(stat_file, t.breakdown_targets, re_targets=True)
            matrix[point] = d
        baseline_df = pd.DataFrame.from_dict(matrix, orient='index')
        baseline_df = baseline_df.reindex(index_order)

        if num_points == 0:
            num_points = len(baseline_df)

        baseline_df.loc['mean'] = baseline_df.iloc[-1]
        baseline_df.loc['mean'][stat] = np.mean(baseline_df[stat])

        data = np.concatenate([baseline_df[stat].values[:-1], [np.NaN],
            baseline_df[stat].values[-1:]])
        print(data.shape)
        data_all.append(data)

    for nc, stat in enumerate(stats):
        stat_dir = stat_dirs[configs_ordered[0]]
        stat_dir = osp.expanduser(stat_dir)
        stat_files = [osp.join(stat_dir, point, 'stats.txt') for point in points]

        matrix = {}
        for point, stat_file in zip(points, stat_files):
            d = c.get_stats(stat_file, t.breakdown_targets, re_targets=True)
            d['mean'] = np.mean(list(d.values()))
            matrix[point] = d

        df = pd.DataFrame.from_dict(matrix, orient='index')
        df = df.reindex(index_order)

        df.loc['mean'] = df.iloc[-1]
        df.loc['mean'][stat] = np.mean(df[stat])
        data = np.concatenate([df[stat].values[:-1],
            [np.NaN], df[stat].values[-1:]])
        print(data/data_all[nc])
        print(data.shape)
        data_all.append(data)


    num_points += 2
    data_all = np.array(data_all)
    print(data_all.shape)

    benchmarks_ordered = []
    for point in df.index:
        if point.endswith('_0'):
            benchmarks_ordered.append(point.split('_')[0])

    xticklabels = [''] * num_points
    print(len(xticklabels))
    for i, benchmark in enumerate(benchmarks_ordered + ['mean']):
        xticklabels[i*strange_const + 1] = benchmark

    print(num_points, num_configs)

    # data_all order:
    # 'Omega16 Queueing', 'Omega16 SSR',
    # 'Omega16-SpecSB Queueing', 'Omega16-SpecSB SSR',

    legends = ['Omega16-OPR', 'Omega16-OPR-SpecSB']
    fig, ax = gm.simple_bar_graph(
            np.array([data_all[0], data_all[2]]),
            xticklabels,
            legends=legends,
            ylabel='Cycles',
            xlim=(-0.5, num_points-0.5),
            title='(b.1) Queueing time reduced by Speculative SB/ARF\non Omega16-OPR',
            colors=['red', 'gray'],
            markers=[7, 6],
            dont_legend=True,
            )

    ax.legend(
            legends,
            loc = 'upper left',
            # bbox_to_anchor=(0, 0),
            ncol=2,
            fancybox=True,
            framealpha=0.5,
            fontsize=13,
            )

    gm.set_cur_ax(gm.ax[2])
    plt.sca(gm.cur_ax)
    fig, ax = gm.simple_bar_graph(
            np.array([data_all[1], data_all[3]]),
            xticklabels,
            legends=legends,
            ylabel='Cycles',
            xlim=(-0.5, num_points-0.5),
            title='(b.2) Wakeup delay reduced by Speculative SB/ARF\non Omega16-OPR',
            colors=['red', 'gray'],
            markers=[7, 6],
            dont_legend=True,
            )

    ax.legend(
            legends,
            loc = 'upper left',
            # bbox_to_anchor=(0, 0),
            ncol=2,
            fancybox=True,
            framealpha=0.5,
            fontsize=13,
            )

def ipc_spec():
    global gm
    gm.set_cur_ax(gm.ax[3])
    plt.sca(gm.cur_ax)

    show_reduction = True

    stat_dirs = {
            'Xbar4': 'xbar4',
            'Xbar4-SpecSB': 'xbar4-rand-hint',
            # 'Xbar4*2-SpecSB': 'dedi-xbar4-rand-hint',
            #'Omega16': 'omega',
            'Omega16-OPR': 'omega-rand',
            'Omega16-OPR-SpecSB': 'omega-rand-hint',
            #'Xbar16': 'xbar',
            #'Xbar16-OPR': 'xbar-rand',
            #'Xbar16-OPR-SpecSB': 'xbar-rand-hint',
            # 'Ideal-OOO': 'ruu-4-issue',
            }
    for k in stat_dirs:
        stat_dirs[k] = c.env.data(f'{stat_dirs[k]}{suffix}')

    configs_ordered = ['Xbar4', 'Xbar4-SpecSB','Omega16-OPR', 'Omega16-OPR-SpecSB']

    benchmarks = [*c.get_spec2017_int(), *c.get_spec2017_fp()]

    points = []
    for b in benchmarks:
        for i in range(0, 3):
            points.append(f'{b}_{i}')

    data_all = []
    num_points, num_configs = 0, len(stat_dirs)
    dfs = dict()
    for config in configs_ordered:
        print(config)
        stat_dir = stat_dirs[config]
        stat_dir = osp.expanduser(stat_dir)
        stat_files = [osp.join(stat_dir, point, 'stats.txt') for point in points]

        matrix = {}
        for point, stat_file in zip(points, stat_files):
            d = c.get_stats(stat_file, t.ipc_target, re_targets=True)
            matrix[point] = d

        df = pd.DataFrame.from_dict(matrix, orient='index')
        df = df.reindex(index_order)

        dfs[config] = df

        if num_points == 0:
            num_points = len(df)

    baseline = 'Xbar4'
    dfs[baseline].loc['rel_geo_mean'] = [1.0]
    print(baseline)
    print(dfs[baseline])
    datas = dict()
    for config in configs_ordered:
        if config != baseline:
            print(config)
            rel = dfs[config]['ipc'] / dfs[baseline]['ipc'][:-1]
            dfs[config]['rel'] = rel

            dfs[config].loc['rel_geo_mean'] = [rel.prod() ** (1/len(rel))] * 2

            if config.endswith('SpecSB'):
                print(dfs[config])
                print(dfs[baseline])
                # dfs[config]['boost'] = dfs[config]['rel'] / dfs[baseline]['rel']

            print(dfs[config])
        data = np.concatenate([dfs[config]['ipc'].values[:-1],
            [np.NaN], dfs[config]['ipc'].values[-1:]])
        datas[config] = data

    legends = ['Omega16-OPR-SpecSB', 'Xbar4-SpecSB', 'Omega16-OPR', 'Xbar4']
    data_all = [datas[x] for x in legends]
    print(data_all)
    data_all = np.array(data_all)
    print(data_all.shape)

    num_points += 2

    benchmarks_ordered = []
    for point in df.index:
        if point.endswith('_0'):
            benchmarks_ordered.append(point.split('_')[0])

    xticklabels = [''] * num_points
    for i, benchmark in enumerate(benchmarks_ordered + ['rel_geomean']):
        xticklabels[i*strange_const + 1] = benchmark

    print(data_all.shape)
    fig, ax = gm.simple_bar_graph(data_all, xticklabels,
            legends,
            ylabel='IPCs',
            xlim=(-0.5, num_points-0.5),
            ylim=(0, 3),
            title='(c) IPC improvements from Speculative SB/ARF\non Omega16-OPR and Xbar4',
            colors=['red', 'gray', 'green', 'blue'],
            markers=['+', 7, 'x', 6],
            with_borders=False,
            dont_legend=True,
            )
    ax.legend(
            legends,
            loc = 'upper left',
            # bbox_to_anchor=(0, 0),
            ncol=2,
            fancybox=True,
            framealpha=0.5,
            fontsize=13,
            )


spec_on_xbar4()
spec_on_omega()
ipc_spec()

plt.tight_layout()

gm.save_to_file("spec_merge")
# plt.show(block=True)
