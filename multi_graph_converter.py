from dxf_to_graph_converter import extract_graph_from_dxf
from multiprocessing import Process
import logging
from pathlib import Path
from networkx import read_yaml
from networkx import compose_all
from networkx import info
from networkx import write_yaml
from collections import defaultdict
import argparse
from util.file_presets import presets

def make_multi_graphs(building):
    logging.basicConfig(level=logging.INFO)
    info = presets[building]
    building_name = info['building_name']
    architecture_files = info['architecture_files']
    label_files = info['label_files']

    for arch_file, label_file in zip(architecture_files, label_files):
        print(arch_file, label_file)
        outfile_name = arch_file.split("/")[-1][:-4]
        print(outfile_name)
        p = Process(
            target=extract_graph_from_dxf,
            kwargs={
                "architecture_filename": arch_file,
                "label_filename": label_file,
                "outfile": f"data/graphs2/{building_name}/"+outfile_name,
                "step_size": 50,
                "building_name": building_name,
            }
        )
        p.start()


def connect_multi_graphs(building_name):
    p = Path(f'data/graphs2/{building_name}/')
    graphs = {}

    for file in p.glob('*.yaml'):
        floor = str(file).split("/")[-1]
        graphs[floor] = read_yaml(str(file))

    print("making super graph")
    super_graph = compose_all(list(graphs.values()))
    print(info(super_graph))

    stair_nodes = []
    elevator_nodes = []
    for node in super_graph.nodes:
        if "RMNAC" in super_graph.nodes[node]:
            if "STAIR" in super_graph.nodes[node]["RMNAC"]:
                stair_nodes.append(node)
            if "ELEV" in super_graph.nodes[node]["RMNAC"]:
                elevator_nodes.append(node)

    elevator_nodes.sort(key= lambda  x : x.floor)
    stair_nodes.sort(key=lambda x: x.floor)
    print("PRINTING ELEVATOR NODES")
    for n in elevator_nodes:
        label = super_graph.nodes[n]["room_label"]
        if "dx" not in label:
            print(n, label)
    print("PRINTING STAIR NODES")
    for n in stair_nodes:
        label = super_graph.nodes[n]["room_label"]
        if "dx" not in label:
            print(n, label)


    # floor_adjacency = defaultdict(list)
    # for i in range(len(floor_ordering)):
    #     if i == 0:
    #         floor_adjacency[floor_ordering[i]] = [floor_ordering[i+1]]
    #     elif i == len(floor_ordering)-1:
    #         floor_adjacency[floor_ordering[i]] = [floor_ordering[i-1]]
    #     else:
    #         floor_adjacency[floor_ordering[i]] = [floor_ordering[i+1], floor_ordering[i-1]]
    #
    # # for node in stair_nodes:
    # #     print(super_graph.nodes[node]["RMNU"])
    # for node in stair_nodes:
    #     for other_node in stair_nodes:
    #         node_name = super_graph.nodes[node]["RMNU"]
    #         other_node_name = super_graph.nodes[other_node]["RMNU"]
    #         if string_distance(
    #                 node_name,
    #                 other_node_name,
    #         ) <= 1 and other_node.floor in floor_adjacency[node.floor]:
    #             # print(f"{node_name}/{node.floor} is connected to {other_node_name}/{other_node.floor}")
    #             super_graph.add_edge(
    #                 u=node,
    #                 v=other_node,
    #                 weight=1,
    #             )
    #
    # for node in elevator_nodes:
    #     for other_node in elevator_nodes:
    #         if node != other_node:
    #             node_name = super_graph.nodes[node]["RMNU"]
    #             other_node_name = super_graph.nodes[other_node]["RMNU"]
    #             if node_name == other_node_name:
    #                 # print(f"Elevator{node_name} is connected to {other_node_name}")
    #                 super_graph.add_edge(
    #                     u=node,
    #                     v=other_node,
    #                     weight=1,
    #                 )

    write_yaml(super_graph, f"data/graphs2/{building_name}.yaml")
    #


def string_distance(a, b):
    distance = 0
    for l1, l2 in zip(a, b):
        if l1 != l2:
            distance += 1

    return distance


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-v', '--verbose', action="store_true", help='turn verbose mode on')
    parser.add_argument('-vv', '--very_verbose', action="store_true", help='turn debug mode on')
    parser.add_argument('-sz', '--step_size', type=int, help="Supply a step size")
    parser.add_argument('-bl', '--building_name', type=str, help="The name of the building for this CAD file")
    args = parser.parse_args()
    if args.verbose:
        logging.basicConfig(level=logging.INFO)
    if args.very_verbose:
        logging.basicConfig(level=logging.DEBUG)

    make_multi_graphs(
    )


# if __name__ == "__main__":
#     make_multi_graphs()
