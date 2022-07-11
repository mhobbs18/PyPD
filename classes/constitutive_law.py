"""
Constitutive law class
----------------------

Notes
-----

"""
import numpy as np
from numba import njit

from solver.constitutive_model import linear


class ConstitutiveLaw():
    """
    Subclass this to define a new constitutive law. This class ensures that
    all constitutive models follow the correct format.
    """

    def __init__():
        pass

    def required_parameters():
        """
        Define the required parameters
        """
        pass

    def calculate_parameter_values():
        """
        Determine the parameter values for the implemented constitutive law
        """
        raise NotImplementedError("This method must be implemented!")

    def calculate_bond_damage():
        """
        Calculate bond damage (softening parameter). The value of d will range
        from 0 to 1, where 0 indicates that the bond is still in the elastic
        range, and 1 represents a bond that has failed
        """
        pass


class Linear():
    """
    Linear constitutive model

    Attributes
    ----------

    Methods
    -------

    Notes
    -----
    * Examine compiling classes with @jitclass
    * How do we employ a material model?
        - bond.material_model.calculate_bond_damage()
    * Should the class inherit from ConstitutiveLaw?
        - class Linear(ConstitutiveLaw):
    """

    def __init__(self, material, particles):
        """
        Linear constitutive model class constructor

        Parameters
        ----------
        material : Material class

        Returns
        -------
        c : float
            Bond stiffness

        sc : float
            Critical stretch

        Notes
        -----
        * TODO: passing an instance of particles is probably bad design and
        should be improved
        """
        self.c = self._calculate_bond_stiffness(material, particles)
        self.sc = self._calculate_critical_stretch(material, particles)

    def _calculate_bond_stiffness(self, material, particles):
        """
        Bond stiffness
            - linear elastic model
            - 2D
            - plane stress

        Parameters
        ----------
        material :
            Instance of material class

        Returns
        -------
        c : float
            Bond stiffness

        Notes
        -----
        """
        t = 2.5E-3  # TODO: do not hardcode values
        c = (9 * material.E) / (np.pi * t * particles.horizon**3)
        return c

    def _calculate_critical_stretch(self, material, particles):
        """
        Critical stretch
            - linear elastic model
            - 2D

        Parameters
        ----------

        Returns
        -------

        Notes
        -----

        """
        sc = np.sqrt((4 * np.pi * material.Gf)
                     / (9 * material.E * particles.horizon))
        return sc

    @staticmethod
    def calculate_bond_damage(sc):
        """
        Calculate bond damage

        Parameters
        ----------
        sc : float

        Returns
        -------
        wrapper : function
            Return a function with the call statement: 
                - calculate_bond_damage(stretch, d)
            The parameters specific to the material model are wrapped...

        Notes
        -----
        """
        @njit
        def wrapper(stretch, d):
            """
            Calculate bond damage

            Parameters
            ----------
            stretch : float
                Bond stretch

            d : float
                Bond damage (softening parameter). The value of d will range
                from 0 to 1, where 0 indicates that the bond is still in the
                elastic range, and 1 represents a bond that has failed

            Returns
            -------
            d : float
                Bond damage (softening parameter). The value of d will range
                from 0 to 1, where 0 indicates that the bond is still in the
                elastic range, and 1 represents a bond that has failed

            Notes
            -----
            * Examine closures and factory functions
            """
            return linear(stretch, d, sc)

        return wrapper

    def calculate_nodal_forces(self):
        """
        Calculate nodal force

        Parameters
        ----------

        Returns
        -------

        Notes
        -----
        * Ideally this method would not be required.
        * Methods in this class should be concerned with the behaviour of a
        single bond
        * Called by particles.calculate_particle_forces()
        """
        pass


class Bilinear(ConstitutiveLaw):
    pass


class Trilinear(ConstitutiveLaw):
    pass


class NonLinear(ConstitutiveLaw):
    pass
