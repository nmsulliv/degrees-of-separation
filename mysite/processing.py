import pickle
from util import Node, QueueFrontier

# Maps names to a set of corresponding person_ids
pickle_in_n = open("mysite/static/pickle/namesdict.pickle","rb")
names = pickle.load(pickle_in_n)

# Maps person_ids to a dictionary of: name, birth, movies (a set of movie_ids)
pickle_in_p = open("mysite/static/pickle/peopledict.pickle","rb")
people = pickle.load(pickle_in_p)

# Maps movie_ids to a dictionary of: title, year, stars (a set of person_ids)
pickle_in_m = open("mysite/static/pickle/moviesdict.pickle","rb")
movies = pickle.load(pickle_in_m)


def load_data(directory):
    """
    Load data from CSV files into memory.
    """
    # Load people
    with open(f"{directory}/people.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            people[row["id"]] = {
                "name": row["name"],
                "birth": row["birth"],
                "movies": set()
            }
            if row["name"].lower() not in names:
                names[row["name"].lower()] = {row["id"]}
            else:
                names[row["name"].lower()].add(row["id"])

    # Load movies
    with open(f"{directory}/movies.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            movies[row["id"]] = {
                "title": row["title"],
                "year": row["year"],
                "stars": set()
            }

    # Load stars
    with open(f"{directory}/stars.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                people[row["person_id"]]["movies"].add(row["movie_id"])
                movies[row["movie_id"]]["stars"].add(row["person_id"])
            except KeyError:
                pass

def display_result(source, target):
    pathway = ""
    result = shortest_path(source, target)
    if result is None:
        pathway = "Not Connected."
    else:
        degrees = len(result)
        degrees_string = "<h2>" + str(degrees) + " degrees of separation  </h2><br>"
        pathway += degrees_string
        result = [(None, source)] + result
        for i in range(degrees):
            person1 = people[result[i][1]]["name"]
            person2 = people[result[i + 1][1]]["name"]
            movie = movies[result[i + 1][0]]["title"]
            current_degree = i + 1
            path_string = "<h3>" + str(current_degree) + ": "+ person1 + " and " + person2 + " starred in " + movie + "<h3>"
            pathway += path_string
    return pathway

def shortest_path(source, target):
    """
    Returns the shortest list of (movie_id, person_id) pairs
    that connect the source to the target.
    If no possible path, returns None.
    """
    frontier = QueueFrontier()
    explored = set()
    path = []
    source_node = Node(source, None, None)

    frontier.add(source_node)
    while ((frontier.empty()) == False):
        parent = frontier.remove()
        explored.add(parent)

        neighbors = neighbors_for_person(parent.state)
        for neighbor in neighbors:
            in_frontier = frontier.contains_state(neighbor[1])
            in_explored = any(parent.state == neighbor[1] for parent in explored)
            if (not in_frontier and not in_explored):
                neighbor_node = Node(neighbor[1], parent, neighbor[0])
                frontier.add(neighbor_node)
                if (neighbor_node.state == target):
                    path = backtrack(path, neighbor_node)
                    return path
    return path


def backtrack(path, target):
    """
    Returns the path of (movie_id, person_id) pairs that
    connect the target to the source.
    """
    pointer = target
    while(pointer.parent is not None):
        pair = (pointer.action, pointer.state)
        path.append(pair)
        pointer = pointer.parent
    path.reverse()
    return path


def person_id_for_name(name):
    """
    Returns the IMDB id for a person's name,
    resolving ambiguities as needed.
    """
    person_ids = list(names.get(name.lower(), set()))
    if len(person_ids) == 0:
        return None
    elif len(person_ids) > 1:
        list_duplicates = "<p>Which " + name + "?<p>"
        for person_id in person_ids:
            person = people[person_id]
            name = person["name"]
            birth = person["birth"]
            person_string = "<p><div class='id'>ID: " + str(person_id) + "</div> Name: " +  name + " | Birth: "+ birth + "<p>"
            list_duplicates += person_string
        return list_duplicates
    else:
        return person_ids[0]

def confirm(name, pid):
    person_ids = list(names.get(name.lower(), set()))
    if pid in person_ids:
        return pid
    else:
        return None

def neighbors_for_person(person_id):
    """
    Returns (movie_id, person_id) pairs for people
    who starred with a given person.
    """
    movie_ids = people[person_id]["movies"]
    neighbors = set()
    for movie_id in movie_ids:
        for person_id in movies[movie_id]["stars"]:
            neighbors.add((movie_id, person_id))
    return neighbors
