# In[0]: Imports
from pathlib import Path
import sys
root_dir = Path(__file__).parent.parent.parent.resolve()
sys.path.append(str(root_dir))
from pyutils.decorators import trim_whitespaces

# In[1] Testing on a list
def test_list():
    l = ['a ', 1.0, '\t 10']
    assert trim_whitespaces(l) == ['a', float(1), '10'], 'Fail to pass the test on list'
    return f'Test on lists - Pass'

test_list()

# In[2] Testing on set
def test_set():
    s = {'a ', 1.0, '\t 10'}
    assert trim_whitespaces(s) == {'a', float(1), '10'}, 'Fail to pass the test on set'
    return f'Test on sets - Pass'

test_set()

# In[3] Testing on tuples
def test_tuple():
    t = ('a ', 1.0, '\t 10')
    assert trim_whitespaces(t) == ('a', float(1), '10'), 'Fail to pass the test on tuple'
    return f'Test on tuples - Pass'

test_tuple()

# In[5] Testing on Dictionaries
def test_dict():
    d={'a ': ' a a a ',
       (1.0, ' 1.0'): '\tb b ',
      '\t 10': 1}
    
    output_dict = {'a': 'a a a',
       (1.0, '1.0'): 'b b',
      '10': 1}
    assert trim_whitespaces(d) == output_dict, f'Fail to pass the test on dictionaries, actual output: {trim_whitespaces(d)}  -  expected: {output_dict}'
    return f'Test on dictionaries - Pass'

test_dict()

# In[6]: Testing the recursion
def test_recursion():

    dct = {
        "1 ": ['a ', 1.0, '\t 10'],
        " a ": {
                 'a ': ' a a a ',
                 (1.0, ' 1.0'): '\tb b ',
                 '\t 10': 1
                }
    }

    expected = {'1': ['a', 1.0, '10'],
               'a':  { 'a': 'a a a',
                       (1.0, '1.0'): 'b b',
                        '10': 1
                        }
                        }

    assert trim_whitespaces(dct) == expected, "Actual output: {trim_whitespaces(d)}  -  Expected: {output_dict}"
    return f'Test on recursion - Pass'

test_recursion()
# In[7]: Testing the homogenous flag
def test_homogenous_1():
    l = ['a ', " ", '\t 10']
    assert trim_whitespaces(l, homogenous=True) == ['a', "", '10'], 'Fail to pass the test on list'
    return f'Test on homogenous1 - Pass'

test_homogenous_1()

# In[8]: Testing the homogenous flag 2

def test_homogenous_2():
    d = {(1., 2.0): ' a a a ',
         ('a ', 'b', ' c'): [1.0, 2.0, 3.0]}
    assert trim_whitespaces(d, homogenous=True) == {(1., 2.0): 'a a a',
                                                    ('a', 'b', 'c'): [1.0, 2.0, 3.0]}, 'Fail to pass the test on list'
    return f'Test on homogenous2 - Pass'


# In[9]: Testing performance with and without the homogenours argument
def test_homogenous_3():
    from timeit import timeit
    from pyutils import trim_whitespaces
    
    l = [f" Name_{i} " for i in range(1_000_000)]

    t1 = timeit("trim_whitespaces(l, homogenous=True)", globals=locals(), number=1)
    t2 = timeit("trim_whitespaces(l, homogenous=False)", globals=locals(), number=1)

    print(f"Homogenous=True took: {t1:.4f} seconds")
    print(f"Homogenous=False took: {t2:.4f} seconds")

test_homogenous_3()


# %%
