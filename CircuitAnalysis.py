# -*- coding: utf-8 -*-
"""
Created on Fri Dec 13 23:08:02 2019

@author: Mahmoud
"""
import numpy as NP


def InterpretCircuit(CircuitString):
    
    Loops = CircuitString.partition(' Common Branches ')[0].split('M ')[1:]
    CommonBranches = CircuitString.partition(' Common Branches ')[2].split('B ')[1:]

    return Loops,CommonBranches

def TotalResistence(Loop):
    Loop = list(filter(lambda string : len(string) != 0,
                       Loop.split(' ')))
    resistive_elements = list(filter(lambda x: x[0] == 'R' or x[0] == 'C' or x[0] == 'L' ,
                                Loop))
    Resistence = 0
    Reactance = 0
    
    for element in resistive_elements:
        if element[0] == 'R':
            Resistence = Resistence + float(element[1:])
        if element[0] == 'L':
            Reactance = Reactance + float(element[1:])
        if element[0] == 'C':
            Reactance = Reactance - float(element[1:])
    
    return complex(Resistence,Reactance)

def CommonResistences(loop_number,CommonBranchesList,number_of_loops):
    transform_each_branchString_to_list = lambda string : list(filter(lambda string : len(string) != 0 , string.split(' ') ))
    
    CommonBranchesList = list(map(transform_each_branchString_to_list,CommonBranchesList))
    
    neighbor_branches = list(filter(lambda branch : int(branch[0]) == loop_number or int(branch[1]) == loop_number,
                                   CommonBranchesList))
        
    CommonResistences = [0 for i in range(0,number_of_loops)]
    
    for branch in neighbor_branches:
        if int(branch[0]) == loop_number:
            CommonResistences[int(branch[1]) - 1] =  -complex(branch[2])
        if int(branch[1]) == loop_number:
            CommonResistences[int(branch[0]) - 1] =  -complex(branch[2])
    
    return CommonResistences

def ResistenceMatrix(Circuit):
    ResistenceMatrix = []
    
    loop_number = 1 
    num_loops = len(Circuit[0])
    for loop in Circuit[0]:        
        
        ResistenceRow = CommonResistences(loop_number,Circuit[1],num_loops)
        ResistenceRow[loop_number - 1] = TotalResistence(loop)
        
        ResistenceMatrix.append(ResistenceRow)
        loop_number = loop_number + 1
        
    return ResistenceMatrix

def VoltageVector(Loops):
        voltage_sources = list(map(lambda string: string[1:string.find(' ')] ,
                                Loops))
        
        return_sum_of_voltages_given_sources = lambda string : sum( map( lambda x : complex(x) , string.split(',') ) )
        
        VoltageVector = list(map( return_sum_of_voltages_given_sources , voltage_sources))
        
        return VoltageVector
        
        

def SolveCircuit(CicuitDescription):
    Circuit = InterpretCircuit(CicuitDescription)

    return NP.linalg.solve( ResistenceMatrix(Circuit) , VoltageVector(Circuit[0]) )

print(SolveCircuit(input()))





















    
    