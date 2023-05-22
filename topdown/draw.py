import pandas as pd
import numpy as np
import utils as u
import matplotlib.pyplot as plt
import matplotlib as mpl
import os
import os.path as osp
# from svglib.svglib import svg2rlg
# from reportlab.graphics import renderPDF

def draw():
    results = {
        # "GEM5-0429":
        #     ("results/gem5-topdown-weighted.csv", "GEM5"),
        "XS-0517": 
            ("results/xs-topdown-weighted.csv", "XS"),
    }

    configs = list(results.keys())

    # colors = ['#83639F', '#EA7827', '#C22F2F', '#449945', '#1F70A9']
    # edge_colors = ['#63437F', '#CA5807', '#A20F0F', '#247925', '#005099']
    color_types = 10
    if color_types == 20:
        cmap = plt.get_cmap('tab20')
        color_index = np.arange(0, 1, 1.0/20)
        colors = [cmap(c) for c in color_index]
        hatches = [None] * 20
    elif color_types == 10:
        cmap = plt.get_cmap('tab10')
        color_index = np.arange(0, 1, 1.0/color_types)
        colors = [cmap(c) for c in color_index] * 3
        hatches = [None] * color_types + ['//']*color_types + ['|']*color_types
    else:
        cmap = plt.get_cmap('Paired')
        color_index = np.arange(0, 1, 1.0/color_types)
        colors = [cmap(c) for c in color_index] * 3
        hatches = [None] * color_types + ['//']*color_types + ['|']*color_types

    # print(colors)

    n_conf = len(configs)
    # Draw stacked bar chart for each simulator
    width = 0.8/n_conf
    # set figure size:

    fig, ax = plt.subplots()
    # fig.set_size_inches(5.77, 3.56)
    # fig.set_size_inches(5.77, 3.0)
    # fig.set_size_inches(7.0, 3.0)
    fig.set_size_inches(8.0, 5.0)

    x = None
    have_set_label = False

    gem5_coarse_rename_map = {
        'NoStall': 'MergeBase',

        # Core
        'LongExecute': 'MergeCore',
        'InstNotReady': 'MergeCore',

        # Memory
        'LoadL1Bound': 'MergeLoad',
        'LoadL2Bound': 'MergeLoad',
        'LoadL3Bound': 'MergeLoad',
        'LoadMemBound': 'MergeLoad',
        'StoreL1Bound': 'MergeStore',
        'StoreL2Bound': 'MergeStore',
        'StoreL3Bound': 'MergeStore',
        'StoreMemBound': 'MergeStore',
        'DTlbStall': 'MergeLoad',

        # Frontend
        'IcacheStall': 'MergeFrontend',
        'ITlbStall': 'MergeFrontend',
        'FragStall': 'MergeFrontend',

        # BP
        'BpStall': 'MergeBadSpec',
        'SquashStall': 'MergeBadSpec',
        'InstMisPred': 'MergeBadSpec',
        'InstSquashed': 'MergeBadSpecInst',

        # BP + backend
        'CommitSquash': 'MergeBadSpec',

        # Unclassified:
        'SerializeStall': 'MergeMisc',
        'TrapStall': 'MergeMisc',
        'IntStall': 'MergeMisc',
        'ResumeUnblock': 'MergeMisc',
        'FetchBufferInvalid': 'MergeFrontend',
        'OtherStall': 'MergeMisc',
        'OtherFetchStall': 'MergeFrontend',
    }
    xs_coarse_rename_map = {
        'OverrideBubble': 'MergeFrontend',
        'FtqFullStall': 'MergeFrontend',
        'FtqUpdateBubble': 'MergeBadSpec',
        'TAGEMissBubble': 'MergeBadSpec',
        'SCMissBubble': 'MergeBadSpec',
        'ITTAGEMissBubble': 'MergeBadSpec',
        'RASMissBubble': 'MergeBadSpec',
        'ICacheMissBubble': 'MergeFrontend',
        'ITLBMissBubble': 'MergeFrontend',
        'BTBMissBubble': 'MergeBadSpec',
        'FetchFragBubble': 'MergeFrontend',

        'DivStall': 'MergeCore',
        'IntNotReadyStall': 'MergeCore',
        'FPNotReadyStall': 'MergeCore',

        'MemNotReadyStall': 'MergeLoad',

        'IntFlStall': 'MergeCore',
        'FpFlStall': 'MergeCore',

        'IntDqStall': 'MergeCore',
        'FpDqStall': 'MergeCore',
        'LsDqStall': 'MergeCore',

        'LoadTLBStall': 'MergeLoad',
        'LoadL1Stall': 'MergeLoad',
        'LoadL2Stall': 'MergeLoad',
        'LoadL3Stall': 'MergeLoad',
        'LoadMemStall': 'MergeLoad',
        'StoreStall': 'MergeStore',

        'AtomicStall': 'MergeMisc',

        'FlushedInsts': 'MergeBadSpecInst',
        'LoadVioReplayStall': 'MergeBadSpec',

        'LoadMSHRReplayStall': 'MergeLoad',

        'ControlRecoveryStall': 'MergeBadSpec',
        'MemVioRecoveryStall': 'MergeBadSpec',
        'OtherRecoveryStall': 'MergeBadSpec',
        
        'OtherCoreStall': 'MergeCoreOther',
        'NoStall': 'MergeBase',

        'MemVioRedirectBubble': 'MergeBadSpec',
        'OtherRedirectBubble': 'MergeMisc',

        'commitInstr': 'Insts',
        'total_cycles': 'Cycles',
    }

    gem5_fine_grain_rename_map = {
        'NoStall': None,

        # Core
        'LongExecute': None,
        'InstNotReady': None,

        # Memory
        'LoadL1Bound': None,
        'LoadL2Bound': None,
        'LoadL3Bound': None,
        'LoadMemBound': None,
        'StoreL1Bound': 'MergeStoreBound',
        'StoreL2Bound': 'MergeStoreBound',
        'StoreL3Bound': 'MergeStoreBound',
        'StoreMemBound': 'MergeStoreBound',
        'DTlbStall': None,

        # Frontend
        'IcacheStall': 'ICacheBubble',
        'ITlbStall': 'ITlbBubble',
        'FragStall': 'FragmentBubble',

        # BP
        'BpStall': 'MergeBadSpecBubble',
        'SquashStall': 'MergeBadSpecBubble',
        'InstMisPred': 'MergeBadSpecBubble',
        'InstSquashed': 'BadSpecInst',

        # BP + backend
        'CommitSquash': 'BadSpecWalking',

        # Unclassified:
        'SerializeStall': None,
        'TrapStall': 'MergeMisc',
        'IntStall': 'MergeMisc',
        'ResumeUnblock': 'MergeMisc',
        'FetchBufferInvalid': 'MergeOtherFrontend',
        'OtherStall': 'MergeMisc',
        'OtherFetchStall': 'MergeOtherFrontend',
    }

    xs_fine_grain_rename_map = {
        'OverrideBubble': 'MergeOtherFrontend',
        'FtqFullStall': 'MergeOtherFrontend',
        'FtqUpdateBubble': 'MergeBadSpecBubble',
        'TAGEMissBubble': 'MergeBadSpecBubble',
        'SCMissBubble': 'MergeBadSpecBubble',
        'ITTAGEMissBubble': 'MergeBadSpecBubble',
        'RASMissBubble': 'MergeBadSpecBubble',
        'ICacheMissBubble': 'ICacheBubble',
        'ITLBMissBubble': 'ITlbBubble',
        'BTBMissBubble': 'MergeBadSpecBubble',
        'FetchFragBubble': 'FragmentBubble',

        'DivStall': 'LongExecute',
        'IntNotReadyStall': 'MergeInstNotReady',
        'FPNotReadyStall': 'MergeInstNotReady',

        'MemNotReadyStall': 'MemNotReady',

        'IntFlStall': 'MergeFreelistStall',
        'FpFlStall': 'MergeFreelistStall',

        'IntDqStall': 'MergeDispatchQueueStall',
        'FpDqStall': 'MergeDispatchQueueStall',
        'LsDqStall': 'MergeDispatchQueueStall',

        'LoadTLBStall': 'DTlbStall',
        'LoadL1Stall': 'LoadL1Bound',
        'LoadL2Stall': 'LoadL2Bound',
        'LoadL3Stall': 'LoadL3Bound',
        'LoadMemStall': 'LoadMemBound',
        'StoreStall': 'MergeStoreBound',

        'AtomicStall': 'SerializeStall',

        'FlushedInsts': 'BadSpecInst',
        'LoadVioReplayStall': None,

        'LoadMSHRReplayStall': None,

        'ControlRecoveryStall': 'MergeBadSpecWalking',
        'MemVioRecoveryStall': 'MergeBadSpecWalking',
        'OtherRecoveryStall': 'MergeBadSpecWalking',
        
        'OtherCoreStall': 'MergeMisc',
        'NoStall': None,

        'MemVioRedirectBubble': 'MergeBadSpecBubble',
        'OtherRedirectBubble': 'MergeMisc',

        'commitInstr': 'Insts',
        'total_cycles': 'Cycles',
    }

    highlight_hatches = {
        # 'layer2_memory_bound-tlb': '///',
    }

    dfs = [pd.read_csv(results[sim_conf][0], index_col=0) for sim_conf in results]
    common_bmk = list(set.intersection(*[set(df.index) for df in dfs]))
    # common_bmk = u.spec_bmks['06']['int']
    # common_bmk = ['bzip2', 'sjeng']
    print(common_bmk)
    dfs = [df.loc[common_bmk] for df in dfs]

    rename = True
    fine_grain_rename = False
    renamed_dfs = []
    for sim_conf, df in zip(results, dfs):
        to_drops = []
        sorted_cols = []

        def rename_with_map(df, rename_map):
            print(df.columns)
            for k in rename_map:
                if rename_map[k] is not None:
                    if rename_map[k].startswith('Merge'):
                        merged = rename_map[k][5:]
                        if merged not in df.columns:
                            df[merged] = df[k]
                            sorted_cols.append(merged)
                        else:
                            df[merged] += df[k]
                    else:
                        df[rename_map[k]] = df[k]
                        sorted_cols.append(rename_map[k])

                    to_drops.append(k)
                else:
                    sorted_cols.append(k)
            print(f'Dropping {to_drops}')
            df.drop(columns=to_drops, inplace=True)

        # Merge df columns according to the rename map if value starting with 'Merge'
        if rename:
            print(f'Renaming columns of {results[sim_conf][1]} stats')
            if fine_grain_rename:
                if results[sim_conf][1] == 'GEM5':
                    rename_with_map(df, gem5_fine_grain_rename_map)
                else:
                    assert results[sim_conf][1] == 'XS'
                    rename_with_map(df, xs_fine_grain_rename_map)
            else:
                if results[sim_conf][1] == 'GEM5':
                    rename_with_map(df, gem5_coarse_rename_map)
                else:
                    assert results[sim_conf][1] == 'XS'
                    rename_with_map(df, xs_coarse_rename_map)
        
                icount = 20*10**6
                print(results[sim_conf][1], f'Base count:\n{df["Base"]}')
                if 'BadSpecInst' in df.columns:
                    df['BadSpecInst'] += df['Base'] - icount
                else:
                    df['BadSpecInst'] = df['Base'] - icount
                print(results[sim_conf][1], f'Bad inst count:\n{df["BadSpecInst"]}')
                df['Base'] = icount

                # df['BadSpec'] = df['BadSpecInst'] + df['BadSpec']
                # df.drop(columns=['BadSpecInst'], inplace=True)


        df = df.astype(float)
        print(df.columns)
        renamed_dfs.append(df)

    common_col = list(set.intersection(*[set(df.columns) for df in renamed_dfs]))
    print(common_col)
    unique_cols = set()
    for sim_conf, df in zip(results, renamed_dfs):
        unique_col = set(df.columns) - set(common_col)
        print(f'{sim_conf}: has unique column: {unique_col}')
        for col in unique_col:
            unique_cols.add(col)
    for df in renamed_dfs:
        for col in unique_cols:
            if col not in df.columns:
                print(f'Adding column {col} to df')
                df[col] = 0.0
        df.sort_index(axis=1, inplace=True)

        

    put_to_front = ['Base', 'BadSpec']
    # excluded = len(put_to_front)
    # colors = colors[excluded:]

    tmp_df = renamed_dfs[0].sort_values(by = 'cpi', ascending=False)
    bmk_sort = tmp_df.index.tolist()
    # bmk_sort = bmk_sort[len(bmk_sort)//2:]
    # bmk_sort = bmk_sort[:len(bmk_sort)//2]

    for sim_conf, df in zip(results, renamed_dfs):

        df = df.loc[bmk_sort]

        # df = df[put_to_front  + [ col for col in df.columns if col not in put_to_front] ]
        df = df[put_to_front + [ col for col in df.columns if col not in put_to_front]]

        # to_drop = ['bmk', 'point', 'workload']
        # df = df.drop(columns=to_drop)
        # drop non-numerical columns
        # df = df.drop(columns=[col for col in df.columns if not col.startswith(
        #     'layer') and not col.startswith('ipc') and not col.startswith('cpi')])

        # if 'ipc' in df.columns:
        #     df_cpi = 1.0/df['ipc']
        #     df = df.mul(df_cpi, axis=0)
        # elif 'cpi' in df.columns:
        #     df_cpi = df['cpi']
        #     df = df.mul(df_cpi, axis=0)
        
        df = df.drop(columns=['cpi'])

        # df = df.div(df['Insts'], axis=0)
        
        # df = df.drop(columns=[col for col in df.columns if not col.startswith('layer')])

        # scale each row to make them sum to 1
        # df = df.div(df.sum(axis=1), axis=0)

        # add rows into one raw
        # df.loc['int overall'] = df.sum(axis=0)
        # df = df.loc[['int overall']]

        # scale each row to make them sum to 1
        # df = df.div(df.sum(axis=1), axis=0)

        # print('CPI stack sum', df.sum(axis=1))
        for to_drop in ['ipc', 'cpi', 'Cycles', 'Insts', 'coverage']:
            if to_drop in df.columns:
                df = df.drop(columns=[to_drop])

        print(df)
        # raise

        # draw stacked bar chart
        bottom = np.zeros(len(df))
        highest = 0.0
        if x is None:
            x = np.arange(len(df), dtype=float)
        for component, color, default_hatch in zip(df.columns, colors[:len(df.columns)], hatches[:len(df.columns)]):
            print(component)
            if component in highlight_hatches:
                hatch = highlight_hatches[component]
            else:
                hatch = default_hatch 
            if have_set_label:
                label = None
            else:
                label = component
            # print('Bottom of astar:', bottom[df.index == 'astar'])
            # if component in ['Base', 'BadSpecInst', 'BadSpec']:
            if True:
                p = ax.bar(x, df[component], bottom=bottom,
                        width=width, color=color, label=label, edgecolor='black', hatch=hatch)
                highest = max(highest, max(bottom + df[component]))
                bottom += df[component]
            # print('New bottom of astar:', bottom[df.index == 'astar'])
        x += width
        have_set_label = True
    # replace x tick labels with df.index with rotation
    ax.set_xticks(x - width * len(results) / n_conf - 0.25)
    ax.set_xticklabels(bmk_sort, rotation=90)
    ax.tick_params(left=False, bottom=False)
    ax.set_ylabel('Slots')
    ax.set_xlabel('SPECCPU 2006 Benchmarks')

    # # set the transparency of frame of legend
    handles, labels = plt.gca().get_legend_handles_labels()
    ax.legend(reversed(handles), reversed(labels), fancybox=True,
              framealpha=0.3,
            #   loc='lower right',
            #   ncol=2,
              loc='best',
              ncol=3,
              )
    # ax.set_title('GEM5 <-- Left, Right --> XS master')
    if n_conf == 2:
        ax.set_title(f'{configs[0]} <-- VS. --> {configs[1]}')
    # ax.set_ylim(0, 4.0)
    # ax.set_ylim(0, highest * 2.2)
    # ax.set_ylim(0, highest * 1.2)
    # ax.set_xlim(-2.5, max(5.5, len(df)) * 2)

    tag = 'compare-topdown'
    # tag = 'int-raw-topdown'
    fig.savefig(osp.join('results', f'{tag}.png'), bbox_inches='tight', pad_inches=0.05, dpi=200)
    # fig.savefig(osp.join('results', f'{tag}.svg'), bbox_inches='tight', pad_inches=0.05)
    # fig.savefig(osp.join('results', f'{tag}.pdf'), bbox_inches='tight', pad_inches=0.05)

    # drawing = svg2rlg(osp.join('results', f'{tag}.svg'))
    # renderPDF.drawToFile(drawing, osp.join('results', f'{tag}.pdf'))
    

if __name__ == '__main__':
    draw()
