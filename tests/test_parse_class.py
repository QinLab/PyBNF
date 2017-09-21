import os
from .context import parse


class TestParse:
    def __init__(self):
        pass

    @classmethod
    def setup_class(cls):
        cls.s = ['job_name =  world #test test', 'verbosity = 3', 'model = strings strings', 'mutate = derp 1 3',
                 ' #derp = derp', 'random_var = var__FREE__ 1 5', 'lognormrandom_var= var2__FREE__ 0.01 1.0e5',
                 'random_var = var3__FREE__ 4 5']

    @classmethod
    def teardown_class(cls):
        pass

    def test_grammar(self):
        assert parse.parse(self.s[0]) == ['job_name', 'world']
        assert parse.parse(self.s[1]) == ['verbosity', '3']
        assert parse.parse(self.s[2]) == ['model', 'strings', 'strings']
        assert parse.parse(self.s[3]) == ['mutate', 'derp', '1', '3']
        assert parse.parse(self.s[5]) == ['random_var', 'var__FREE__', '1', '5']
        assert parse.parse(self.s[6]) == ['lognormrandom_var', 'var2__FREE__', '0.01', '1.0E5']
        assert parse.parse(self.s[7]) == ['random_var', 'var3__FREE__', '4', '5']

    def test_capital(self):
        assert parse.parse('Model = string string') == ['model', 'string', 'string']
        assert parse.parse('Job_name = string') == ['job_name', 'string']
        assert parse.parse('vErbosity = 2') == ['verbosity', '2']

    def test_ploop(self):
        d = parse.ploop(self.s)
        assert 'job_name' in d.keys()
        assert 'verbosity' in d.keys()
        assert 'model' in d.keys()
        assert ('lognormrandom_var', 'var2__FREE__') in d.keys()
        assert ('random_var', 'var__FREE__') in d.keys()
        assert ('random_var', 'var3__FREE__') in d.keys()

        assert d['job_name'] == 'world'
        assert d['verbosity'] == '3'
        assert d['model'] == ['strings', 'strings']
        assert d[('mutate', 'derp')] == ['1', '3']
        assert d[(('random_var', 'var3__FREE__'))] == ['4', '5']