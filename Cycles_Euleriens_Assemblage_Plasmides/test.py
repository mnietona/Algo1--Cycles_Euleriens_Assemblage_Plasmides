def __equal_mod_rotation(s1, s2):
    if len(s1) != len(s2):
        return False
    from difflib import SequenceMatcher
    i, j, k = SequenceMatcher(None, s1, s2).find_longest_match()
    tmp = s1[i+k:] + s1[:i]
    return tmp.startswith(s2[j+k:]) and tmp.endswith(s2[:j])

def __import_into_global(mod, name):
    import importlib
    globals()[name] = importlib.import_module(mod).__dict__[name]

def get_stdout(callback, *args, **kwargs):
    with StringIO() as buffer, redirect_stdout(buffer):
        callback(*args, **kwargs)
        return str(buffer.getvalue())

test_files = {
    '1': ['CAACAC'],
    '2': ['CAACAC', 'ACACAC', 'CACAAA', 'CAAACC'],
    'CTAGCACATG': ['ATGCTA', 'GCTAGC', 'TAGCAC', 'GCACAT', 'ACATGC'],
}

def __id2path(id_):
    return f'__tmp_test{id_}.txt'

def create_file(id_):
    if not isinstance(id_, str):
        id_ = str(id_)
    assert id_ in test_files
    with open(__id2path(id_), 'w') as f:
        for line in test_files[id_]:
            f.write(line)
            f.write('\n')

def remove_file(id_):
    import os
    os.remove(__id2path(id_))

def requires_test_file(id_):
    def decorator(func):
        from functools import wraps
        @wraps(func)
        def wrapper(*args, **kwargs):
            create_file(id_)
            interrupted = False
            try:
                ret = func(*args, **kwargs)
            except Exception as e:
                interrupted = True
                ret = e
            remove_file(id_)
            if interrupted:
                raise ret
            else:
                return ret
        return wrapper
    return decorator

########## À COMPLÉTER ##########

def num_edges(G):
    ''' Renvoie le nombre d'arcs dans G '''
    return len(G.arcs())

def are_linked(G, u, v):
    ''' Renvoie True si G contient un arc de u vers v et False sinon '''
    if (u,v) in G.arcs():
        return True
    else:
        return False

########## DÉBUT DES TESTS ##########

def test_imports():
    from matrix import SparseCSCMatrix
    from graph import Graph
    names = ('load_reads', 'construct_graph', 'eulerian_cycle', 'reconstruct_plasmid')
    for name in names:
        try:
            __import_into_global('projet3', name)
        except (ImportError, NameError, KeyError) as e:
            assert False, f'Impossible d\'importer projet3.' + str(e).replace("'", '')

def __test_load_reads(id_):
    assert test_files[id_] == load_reads(__id2path(id_))

@requires_test_file('1')
def test_load_reads_single_word():
    __test_load_reads('1')

@requires_test_file('2')
def test_load_reads_multiple_words():
    __test_load_reads('2')

@requires_test_file('CTAGCACATG')
def test_load_reads_trivial_plasmid():
    __test_load_reads('CTAGCACATG')

def __test_db_graph(G, edges):
    for u, v in edges:
        assert are_linked(G, u, v)
    assert num_edges(G) == len(edges)

@requires_test_file('1')
def test_db_graph_single_word_k2():
    G = construct_graph(load_reads(__id2path('1')), 2)
    edges = [
        ('A', 'A'), ('A', 'C'), ('C', 'A')
    ]
    __test_db_graph(G, edges)

@requires_test_file('2')
def test_db_graph_multiples_words_k2():
    G = construct_graph(load_reads(__id2path('2')), 2)
    edges = [
        ('A', 'A'), ('A', 'C'), ('C', 'A'), ('C', 'C')
    ]
    __test_db_graph(G, edges)

@requires_test_file('1')
def test_db_graph_single_word_k3():
    G = construct_graph(load_reads(__id2path('1')), 3)
    edges = [
        ('AA', 'AC'), ('AC', 'CA'), ('CA', 'AA'), ('CA', 'AC')
    ]
    __test_db_graph(G, edges)

@requires_test_file('2')
def test_db_graph_multiples_words_k3():
    G = construct_graph(load_reads(__id2path('2')), 3)
    edges = [
        ('AA', 'AA'), ('AA', 'AC'),
        ('AC', 'CA'), ('AC', 'CC'),
        ('CA', 'AC'), ('CA', 'AA')
    ]
    __test_db_graph(G, edges)

@requires_test_file('1')
def test_db_graph_single_word_k4():
    G = construct_graph(load_reads(__id2path('1')), 4)
    edges = [
        ('CAA', 'AAC'), ('AAC', 'ACA'), ('ACA', 'CAC')
    ]
    __test_db_graph(G, edges)

@requires_test_file('2')
def test_db_graph_multiples_words_k4():
    G = construct_graph(load_reads(__id2path('2')), 4)
    edges = [
        ('AAA', 'AAC'),
        ('AAC', 'ACA'), ('AAC', 'ACC'),
        ('ACA', 'CAA'), ('ACA', 'CAC'),
        ('CAA', 'AAC'), ('CAA', 'AAA'),
        ('CAC', 'ACA')
    ]
    __test_db_graph(G, edges)

@requires_test_file('CTAGCACATG')
def test_db_graph_trivial_plasmid():
    G = construct_graph(load_reads(__id2path('CTAGCACATG')), 4)
    verts = ['ATG', 'TGC', 'GCT', 'CTA', 'TAG', 'AGC', 'GCA', 'CAC', 'ACA', 'CAT']
    edges = [(verts[i], verts[(i+1)%len(verts)]) for i in range(len(verts))]
    __test_db_graph(G, edges)

@requires_test_file('CTAGCACATG')
def test_reconstruction_trivial_plasmid_k3():
    G = construct_graph(load_reads(__id2path('CTAGCACATG')), 3)
    assert __equal_mod_rotation(reconstruct_plasmid(eulerian_cycle(G)), 'CTAGCACATG')

@requires_test_file('CTAGCACATG')
def test_reconstruction_trivial_plasmid_k4():
    G = construct_graph(load_reads(__id2path('CTAGCACATG')), 4)
    assert __equal_mod_rotation(reconstruct_plasmid(eulerian_cycle(G)), 'CTAGCACATG')

@requires_test_file('CTAGCACATG')
def test_reconstruction_trivial_plasmid_k5():
    G = construct_graph(load_reads(__id2path('CTAGCACATG')), 5)
    assert __equal_mod_rotation(reconstruct_plasmid(eulerian_cycle(G)), 'CTAGCACATG')

@requires_test_file('CTAGCACATG')
def test_program_execution():
    import subprocess
    assert __equal_mod_rotation(
        subprocess.check_output(['python3', 'projet3.py', '-f', __id2path('CTAGCACATG'), '-k4']).decode('UTF-8').strip(),
        'CTAGCACATG'
    )
