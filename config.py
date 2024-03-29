class Config():
    """
    Klasa przechowująca informację o aktualnie używanej konfiguracji.
    """
    def __init__(
                self, 
                population_size = 1000, 
                mutation_prob = 0.1, 
                parents_ratio = 0.5, 
                include_parents = False,
                max_iter = 130
    ):
        self.population_size = population_size
        self.mutation_prob = mutation_prob
        self.parents_ratio = parents_ratio
        self.include_parents = include_parents
        self.max_iter = max_iter

    def update(self, params):
        for param_name, param_value in params.items():
            setattr(self, param_name, param_value)

    def __repr__(self):
        return "CONFIG:\n" + "\n".join("{}={!r}".format(k, v) for k, v in self.__dict__.items())