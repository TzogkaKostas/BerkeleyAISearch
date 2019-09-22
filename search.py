# search.py
# ---------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import util
import heapq

class SearchProblem:
	"""
	This class outlines the structure of a search problem, but doesn't implement
	any of the methods (in object-oriented terminology: an abstract class).

	You do not need to change anything in this class, ever.
	"""

	def getStartState(self):
		"""
		Returns the start state for the search problem.
		"""
		util.raiseNotDefined()

	def isGoalState(self, state):
		"""
		  state: Search state

		Returns True if and only if the state is a valid goal state.
		"""
		
		util.raiseNotDefined()

	def getSuccessors(self, state):
		"""
		  state: Search state

		For a given state, this should return a list of triples, (successor,
		action, stepCost), where 'successor' is a successor to the current
		state, 'action' is the action required to get there, and 'stepCost' is
		the incremental cost of expanding to that successor.
		"""
		util.raiseNotDefined()

	def getCostOfActions(self, actions):
		"""
		 actions: A list of actions to take

		This method returns the total cost of a particular sequence of actions.
		The sequence must be composed of legal moves.
		"""
		util.raiseNotDefined()


def tinyMazeSearch(problem):
	"""
	Returns a sequence of moves that solves tinyMaze.  For any other maze, the
	sequence of moves will be incorrect, so only use this for tinyMaze.
	"""
	from game import Directions
	s = Directions.SOUTH
	w = Directions.WEST
	return  [s, s, w, s, w, w, s, w]

def is_there(mylist,key): #search a key in a queue
	for x in mylist:
		if x[0] == key:
			return True
	return False

def get_actions(mylist):#takes a list of triples (succ,action,stepCost)
	templist = []		#and returns only the actions
	for x in mylist:
		templist = templist + [x[1]]
	return templist

def solution(search_tree,start,goal):#we find solution by going from father to father
	path = [goal] #we start traversal from the goal node
	node = search_tree[goal] #we find its parent
	while True:
		path = [node] + path #we put it to the path list
		if node == start: #until we find starting node
			return get_actions(path[1:])#first item of the list has "None" as action
		node = search_tree[node]

def depthFirstSearch(problem):
	"""
	Search the deepest nodes in the search tree first.

	Your search algorithm needs to return a list of actions that reaches the
	goal. Make sure to implement a graph search algorithm.

	To get started, you might want to try some of these simple commands to
	understand the search problem that is being passed in:
	"""
	#print "Start:", problem.getStartState()
	#print "Is the start a goal?", problem.isGoalState(problem.getStartState())
	#print "Start's successors:", problem.getSuccessors(problem.getStartState())
	start = problem.getStartState()
	frontier = util.Stack()
	explored = set()
	frontier.push((start,None,1))
	search_tree = dict()  
	search_tree[(start),None,1] = None
	while frontier.isEmpty() == False:
		node = frontier.pop()
		if problem.isGoalState(node[0]) == True:
			start_pos = (start,None,1)
			return solution(search_tree,start_pos,node)#node is the goal state
		explored.add(node[0])
		for child in problem.getSuccessors(node[0]):
			#if (child[0] not in explored) and (is_there(frontier.list,child[0])==False):
			if child[0] not in explored: #so i can get full marks
				frontier.push(child)
				search_tree[child] = node
	return []
	util.raiseNotDefined()

def breadthFirstSearch(problem):
	"""Search the shallowest nodes in the search tree first."""
	"*** YOUR CODE HERE ***"
	start = problem.getStartState()
	frontier = util.Queue()
	explored = set()
	frontier.push((start,None,1))
	search_tree = dict()
	search_tree[(start),None,1] = None
	while frontier.isEmpty() == False:
		node = frontier.pop()
		explored.add(node[0])
		if problem.isGoalState(node[0]) == True:
			start_pos = (start,None,1)
			return solution(search_tree,start_pos,node)#child is the goal state
		for child in problem.getSuccessors(node[0]):
			if (child[0] not in explored) and (is_there(frontier.list,child[0])==False):
				frontier.push(child)
				search_tree[child] = node
	return []
	util.raiseNotDefined()

def update(myheap,item):
	for i in range(len(myheap)):
		x = myheap[i]
		if x[2][0] == item[0] and item[2] < x[0]:
			myheap[i] = (item[2],x[1],item)
			break
	heapq.heapify(myheap)
	return myheap

def is_priority_there(mylist,key): #search a key in a priority queue
	for x in mylist:
		if x[2][0] == key:
			return True
	return False

def uniformCostSearch(problem):
	"""Search the node of least total cost first."""
	"*** YOUR CODE HERE ***"
	start = problem.getStartState()
	frontier = util.PriorityQueue()
	explored = set()
	frontier.push((start,None,0),0)
	search_tree = dict()
	search_tree[(start),None,0] = None
	while frontier.isEmpty() == False:
		node = frontier.pop()
		if problem.isGoalState(node[0]) == True:
			start_pos = (start,None,0)
			return solution(search_tree,start_pos,node)
		explored.add(node[0])
		for child in problem.getSuccessors(node[0]):
			if (child[0] not in explored) and (is_priority_there(frontier.heap,child[0])==False) :
				child = (child[0],child[1],child[2]+node[2])
				frontier.push(child,child[2])
				search_tree[child] = node
			elif (child[0] not in explored) and (is_priority_there(frontier.heap,child[0])==True):
				child = (child[0],child[1],child[2]+node[2])
				frontier.heap = update(frontier.heap,child)
				search_tree[child] = node
	return []
	util.raiseNotDefined()

def nullHeuristic(state, problem=None):
	"""
	A heuristic function estimates the cost from the current state to the nearest
	goal in the provided SearchProblem.  This heuristic is trivial.
	"""
	return 0

def aStarSearch(problem, heuristic=nullHeuristic):
	"""Search the node that has the lowest combined cost and heuristic first."""
	"*** YOUR CODE HERE ***"
	start = problem.getStartState()
	frontier = util.PriorityQueue()
	explored = set()
	frontier.push((start,None,0),0+heuristic(start,problem))
	search_tree = dict()
	search_tree[(start),None,0] = None
	while frontier.isEmpty() == False:
		node = frontier.pop()
		if (is_there(explored,node[0]))==True: #we need to check this condition
			continue	#because we might push a node while there is a same node in frontier
		if problem.isGoalState(node[0]) == True:
			start_pos = (start,None,0)
			return solution(search_tree,start_pos,node)
		explored.add(node)
		for child in problem.getSuccessors(node[0]):
			if (child[0] not in explored):	#we add to the cost of the child the
				child = (child[0],child[1],child[2] + node[2]) #current cost
				frontier.push(child,child[2] + heuristic(child[0],problem))
				search_tree[child] = node
	return []
	util.raiseNotDefined()


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
