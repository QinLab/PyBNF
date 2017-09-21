import numpy as np
import pybnf.data as data
import warnings


class ObjectiveFunction(object):
    """
    Abstract class representing an objective function
    """

    def evaluate_multiple(self, sim_data_list, exp_data_list):
        """
        Compute the value of the objective function on several data sets, and return the total.

        You may also call this function with single Data objects instead of iterables.

        :param sim_data_list: List of simulation Data objects
        :type sim_data_list: iterable
        :param exp_data_list: List of the corresponding experimental Data objects
        :type exp_data_list: iterable
        :return:
        """
        if type(sim_data_list) == data.Data:
            return self.evaluate(sim_data_list, exp_data_list)

        total = 0.
        for (sim_data, exp_data) in zip(sim_data_list, exp_data_list):
            total += self.evaluate(sim_data, exp_data)
        return total

    def evaluate(self, sim_data, exp_data):
        """
        :param sim_data: A Data object containing simulated data
        :type sim_data: Data
        :param exp_data: A Data object containing experimental data
        :type exp_data: Data
        :return: float, value of the objective function, with a lower value indicating a better fit.
        """
        raise NotImplementedError("Subclasses must override evaluate()")


class ChiSquareObjective(ObjectiveFunction):
    def evaluate(self, sim_data, exp_data):
        """
        :param sim_data: A Data object containing simulated data
        :type sim_data: Data
        :param exp_data: A Data object containing experimental data
        :type exp_data: Data
        :return: float, value of the objective function, with a lower value indicating a better fit.
        """

        indvar = min(exp_data.cols, key=exp_data.cols.get)  # Get the name of column 0, the independent variable

        compare_cols = set(exp_data.cols).intersection(set(sim_data.cols))  # Set of columns to compare
        compare_cols.remove(indvar)

        # TODO: Warn if experiment columns are going unused

        func_value = 0.0
        # Iterate through rows of experimental data
        for rownum in range(exp_data.data.shape[0]):
            sim_row = sim_data.get_row(indvar,
                                       exp_data.data[rownum, 0])  # The simulation row corresponding to this expt row.
            if sim_row is None:
                warnings.warn("Ignored " + indvar + " " + str(exp_data.data[rownum, 0]) +
                              " because that " + indvar + " was not in the simulation data.", RuntimeWarning)
                continue

            for col_name in compare_cols:
                sim_val = sim_row[sim_data.cols[col_name]]
                exp_val = exp_data.data[rownum, exp_data.cols[col_name]]
                exp_sigma = exp_data.data[rownum, exp_data.cols[col_name + '_SD']]
                if np.isnan(exp_val):
                    continue
                # TODO: handle nan simulation values
                # TODO: more informative error if _SD is missing

                func_value += 1. / (2. * exp_sigma ** 2.) * (sim_val - exp_val) ** 2.

        return func_value