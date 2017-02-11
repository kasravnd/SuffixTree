"""An optimized implementation of Suffix-Tree."""

from operator import attrgetter
from itertools import count
from collections import OrderedDict


class Node:
    """The Suffix-tree's node."""

    def __init__(self):
        # self.__identifier = identifier
        self.children = dict.fromkeys(chr(i) for i in range(0, 256))
        # for leaf nodes, it stores the index of suffix for
        # the path  from root to leaf"""
        self.suffixIndex = None
        self.start = None
        self.end = None
        self.suffixLink = None

    def __eq__(self, node):
        atg = attrgetter('start', 'end', 'suffixIndex')
        return atg(self) == atg(node)

    def __ne__(self, node):
        atg = attrgetter('start', 'end', 'suffixIndex')
        return atg(self) != atg(node)

'''
class Edge:
    """Enge of suffix-tree."""

    def __init__(self, start_node, end_node, label, identifier):
        self._start = start_node
        self._end = end_node
        self._label = label
        self._first_char = label[0]
        self._identifier = identifier

    def __eq__(self, edge):
        atgt = attrgetter('_start', '_end', '_first_char')
        return atgt(edge) == atgt(self)

    def is_leaf(self):
        """Check if an edge is leaf."""
        return bool(self._end)

    def __str__(self):
        return self._label

    @property
    def identifier(self):
        return self._identifier

    def append(self, char):
        self._label += char

    def is_root_leaf(self):
        return self._start.identifier == 0 and self._end is None
'''


class SuffixTree:
    """The Suffix-Tree."""

    def __init__(self, data):
        """Initiate the tree."""
        self._string = data
        self.lastNewNode = None
        self.activeNode = None
        self.max_char = 256
        """activeEdge is represeted as input string character
          index (not the character itself)"""
        self.activeEdge = -1
        self.activeLength = 0
        # remainingSuffixCount tells how many suffixes yet to
        # be added in tree
        self.remainingSuffixCount = 0
        self.leafEnd = -1
        self.rootEnd = None
        self.splitEnd = None
        self.size = -1  # Length of input string
        self.root = self.create_root()

    def edge_length(self, node):
        return node.end - node.start + 1

    def walk_down(self, current_node):
        """Walk down from current node.

        activePoint change for walk down (APCFWD) using
        Skip/Count Trick  (Trick 1). If activeLength is greater
        than current edge length, set next  internal node as
        activeNode and adjust activeEdge and activeLength
        accordingly to represent same activePoint.
        """
        if (self.activeLength >= self.edge_length(current_node)):
            self.activeEdge += self.edge_length(current_node)
            self.activeLength -= self.edge_length(current_node)
            self.activeNode = current_node
            return True
        return False

    def node_counter(self):
        return next(self._node_count)

    def edge_counter(self):
        return next(self._edge_count)

    def create_root(self):
        node = Node()
        node.start = -1
        node.end = self.rootEnd
        """suffixIndex will be set to -1 by default and
           actual suffix index will be set later for leaves
           at the end of all phases"""
        node.suffixIndex = -1
        node.suffixLink = node
        return node

    def new_node(self, start, end):
        """For root node, suffixLink will be set to NULL
        For internal nodes, suffixLink will be set to root
        by default in  current extension and may change in
        next extension"""
        node = Node()
        node.suffixLink = self.root
        node.start = start
        node.end = end
        """suffixIndex will be set to -1 by default and
           actual suffix index will be set later for leaves
           at the end of all phases"""
        node.suffixIndex = -1
        return node

    def extend_suffix_tree(self, pos):
        """Extension Rule 1, this takes care of extending all
        leaves created so far in tree"""
        self.leafEnd = pos
        """Increment remainingSuffixCount indicating that a
        new suffix added to the list of suffixes yet to be
        added in tree"""
        self.remainingSuffixCount += 1
        """set lastNewNode to None while starting a new phase,
         indicating there is no internal node waiting for
         it's suffix link reset in current phase"""
        self.lastNewNode = None
        # Add all suffixes (yet to be added) one by one in tree
        while(self.remainingSuffixCount > 0):
            if (self.activeLength == 0):
                self.activeEdge = pos  # APCFALZ
            #  There is no outgoing edge starting with
            #  activeEdge from activeNode
            if (self.activeNode.children[self._string[self.activeEdge]] is None):
                # Extension Rule 2 (A new leaf edge gets created)
                self.activeNode.children[self._string[self.activeEdge]] = self.new_node(pos, self.leafEnd)
                """A new leaf edge is created in above line starting
                 from  an existng node (the current activeNode), and
                 if there is any internal node waiting for it's suffix
                 link get reset, point the suffix link from that last
                 internal node to current activeNode. Then set lastNewNode
                 to None indicating no more node waiting for suffix link
                 reset."""
                if (self.lastNewNode is not None):
                    self.lastNewNode.suffixLink = self.activeNode
                    self.lastNewNode = None
            #  There is an outgoing edge starting with activeEdge
            #  from activeNode
            else:
                #  Get the next node at the end of edge starting
                #  with activeEdge
                _next = self.activeNode.children[self._string[self.activeEdge]]
                if self.walk_down(_next):  # Do walkdown
                    # Start from _next node (the new activeNode)
                    continue
                """Extension Rule 3 (current character being processed
                  is already on the edge)"""
                if (self._string[_next.start + self.activeLength] == self._string[pos]):
                    # If a newly created node waiting for it's
                    # suffix link to be set, then set suffix link
                    # of that waiting node to curent active node
                    if((self.lastNewNode is not None) and (self.activeNode != self.root)):
                        self.lastNewNode.suffixLink = self.activeNode
                        self.lastNewNode = None
                    # APCFER3
                    self.activeLength += 1
                    """STOP all further processing in this phase
                    and move on to _next phase"""
                    break
                """We will be here when activePoint is in middle of
                  the edge being traversed and current character
                  being processed is not  on the edge (we fall off
                  the tree). In this case, we add a new internal node
                  and a new leaf edge going out of that new node. This
                  is Extension Rule 2, where a new leaf edge and a new
                internal node get created"""
                self.splitEnd = _next.start + self.activeLength - 1
                # New internal node
                split = self.new_node(_next.start, self.splitEnd)
                self.activeNode.children[self._string[self.activeEdge]] = split
                # New leaf coming out of new internal node
                split.children[self._string[pos]] = self.newNode(pos, self.leafEnd)
                _next.start += self.activeLength
                split.children[self._string[_next.start]] = _next
                """We got a new internal node here. If there is any
                  internal node created in last extensions of same
                  phase which is still waiting for it's suffix link
                  reset, do it now."""
                if (self.lastNewNode is not None):
                    # suffixLink of lastNewNode points to current newly
                    # created internal node
                    self.lastNewNode.suffixLink = split
                """Make the current newly created internal node waiting
                  for it's suffix link reset (which is pointing to self.root
                  at present). If we come across any other internal node
                  (existing or newly created) in next extension of same
                  phase, when a new leaf edge gets added (i.e. when
                  Extension Rule 2 applies is any of the next extension
                  of same phase) at that point, suffixLink of this node
                  will point to that internal node."""
                self.lastNewNode = split
            """One suffix got added in tree, decrement the count of
               suffixes yet to be added."""
            self.remainingSuffixCount -= 1
            if ((self.activeNode == self.root) and (self.activeLength > 0)):  # APCFER2C1
                self.activeLength -= 1
                self.activeEdge = pos - self.remainingSuffixCount + 1
            elif (self.activeNode != self.root):  # APCFER2C2
                self.activeNode = self.activeNode.suffixLink

    def set_suffix_index_by_DFS(self, n, label_height):
        if n is None:
            return

        if n.start != -1:  # A non-root node
            # Print the label on edge from parent to current node
            print((n.start, n.end))

        leaf = 1
        for i in range(self.max_char):
            if n.children[chr(i)] is not None:
                if leaf == 1 and n.start != -1:
                    print(" [{}]\n".format(n.suffixIndex))

                # Current node is not a leaf as it has outgoing
                # edges from it.
                leaf = 0
                self.set_suffix_index_by_DFS(n.children[chr(i)],
                                             label_height + self.edge_length(n.children[chr(i)]))

        if leaf == 1:
            n.suffixIndex = self.size - label_height
            print(" [{}]\n".format(n.suffixIndex))

    def print_dfs(self, current):
        start, end = current.start, current.end
        yield self._string[start: end]

        for node in current.children.values():
            if node:
                yield from self.walk(node)

    def build_suffix_tree(self):
        self.size = len(self._string)

        """Root is a special node with start and end indices as -1,
        as it has no parent from where an edge comes to root"""
        self.rootEnd = -1

        self.activeNode = self.root  # First activeNode will be root
        for i in range(self.size):
            self.extend_suffix_tree(i)
        self.set_suffix_index_by_DFS(self.root, 0)

        # Free the dynamically allocated memory
        # self.free_suffix_tree_by_postorder(root)

    def __str__(self):
        return "\n".join(map(str, self.edges.values()))


s = "abcabxabcd$"
tree = SuffixTree(s)
tree.build_suffix_tree()
# print("\n".join(tree.print_dfs(tree.root)))
