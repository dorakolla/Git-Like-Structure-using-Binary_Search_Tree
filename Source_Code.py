from os import unlink
class Node:
    def __init__(self, name=None, parent=[None, None], left=None, right=None):
        self.name = name
        self.left = left
        self.right = right
        self.parent = {parent[0]: parent[1]}

    def New_file(self, data):
        file = open((self.name + ".txt"), mode="w")
        file.write(data)
        file.close()

    def get_Data(self):
        file = open((self.name + ".txt"), mode="r")
        lines = file.readlines()
        data = ""
        for line in lines:
            data += line
        file.close()
        return data

    def delete_File(self):
        file = open((self.name + ".txt"), mode="w")
        file.close()
        unlink(file.name)

    def minimum(self):
        if self.left is None:
            return self
        return self.left.minimum()

    def maximum(self):
        if self.right is None:
            return self
        return self.right.maximum()

    def successor(self, branch):
        if self.right is not None:
            return self.right.minimum()
        if self.parent[branch] is None:
            return None
        x = self
        y = x.parent[branch]
        while y is not None and x != y.left:
            x = y
            y = y.parent[branch]
        return

    def predecessor(self, branch):
        if self.left is not None:
            return self.left.maximum()
        if self.parent[branch] is None:
            return None
        x = self
        y = x.parent[branch]
        while y is not None and x != y.right:
            x = y
            y = y.parent[branch]
        return y

    def search(self, k):
        if self.name == k:
            return self
        elif self.name > k:
            if self.left is not None:
                return self.left.search(k)
            else:
                return None
        else:
            if self.right is not None:
                return self.right.search(k)
            else:
                return None

    def Inorder(self):
        if self.left is not None:
            self.left.Inorder()
        print(self.name)
        if self.right is not None:
            self.right.Inorder()

    def isLeftChild(self, branch):
        if self.parent[branch] is None:
            return False
        if self.parent[branch].left is not None and self.parent[branch].left.name == self.name:
            return True
        return False

    def isRightChild(self, branch):
        if self.parent[branch] is None:
            return False
        if self.parent[branch].right is not None and self.parent[branch].right.name == self.name:
            return True
        return False
    def __del__(self):
        self.delete_File()


class BST:
    def __init__(self):
        self.branches = {"master": None}

    def insertion(self, key, branch):
        root = self.branches[branch]
        if root is None:
            temp = self.branches[branch] = Node(key, [branch, None])
            data = data_Input("Enter data: ")
            temp.New_file(data)
            return
        temp = root
        while True:
            if temp.name > key:
                if temp.left is None:
                    temp.left = Node(key, [branch, temp])
                    data = data_Input("Enter data: ")
                    temp.left.New_file(data)
                    return
                else:
                    temp = temp.left
            else:
                if temp.right is None:
                    temp.right = Node(key, [branch, temp])
                    data = data_Input("Enter data: ")
                    temp.right.New_file(data)
                    return
                else:
                    temp = temp.right

    def deletion(self, key, branch):
        temp = self.branches[branch]
        if temp is None:
            print("File doesn't exist!")
            return
        while True:
            if temp.name == key:
                if temp.left is not None:
                    pred = temp.left.maximum()
                    temp.name = pred.name
                    temp.New_file(pred.get_Data())
                    temp = temp.left
                    key = pred.name
                elif temp.right is not None:
                    suc = temp.right.minimum()
                    temp.name = suc.name
                    temp.New_file(suc.get_Data())
                    temp = temp.right
                    key = suc.name
                else:
                    temp.delete_File()
                    print("File deleted")
                    if temp.isLeftChild(branch):
                        temp.parent[branch].left = None
                    elif temp.isRightChild(branch):
                        temp.parent[branch].right = None
                    else:
                        self.branches[branch] = None
                    del temp.parent[branch]
                    return
            elif temp.name > key:
                if temp.left is None:
                    print("File doesn't exist!")
                    return
                temp = temp.left
            else:
                if temp.right is None:
                    print("File doesn't exist!")
                    return
                temp = temp.right
    def edit(self, key, branch):
        temp = self.branches[branch]
        while True:
            if temp.name==key:
               previous_data=temp.get_Data()
               print("Enter '0' to edit previos data  :")
               print("Enter '1' to Enter new data  :")
               inp=input("Enter choice  :")
               if inp=="0":
                    print("previous Data")
                    print(previous_data)
                    data=data_Input("Enter new data :" )
                    temp.New_file(data)
                    return
               elif inp=="1":
                   data=data_Input("Enter new data :" )
                   temp.New_file(data)
                   return
            elif temp.name>key:
                if temp.left is not None:
                   temp = temp.left
            else:
                if temp.right is not None:
                   temp = temp.right
        
        
            
    def search(self, k, branch):
        node = self.branches[branch]
        if node is not None:
            return node.search(k)

    def Inorder1(self, branch):
        root = self.branches[branch]
        if root is not None:
            root.Inorder()

    def New_Branch(self, branch, Previous_Branch):
        tree1 = self.branches[Previous_Branch]
        self.branches[branch] = tree1
def data_Input(prompt):
    data = ""
    print(prompt, end="")
    while True:
        line = input()
        if line == "-1":
            break
        data += line + "\n"
    return data

Tree = BST()
current_Branch = "master"
Previous_Branch = None
branches = ["master"]
        
while True:
    print("\nCurrent Branch:", current_Branch)
    print("\n1. List Files\n2. View File\n3. New File\n4. Delete File\n5. Edit file\n6. List Branches\n7. New "
          "Branch\n8. Switch Branch\n9. Exit\n")
    choice = input("$ ")
    print()
    if choice == "1":
        print("Files: ")
        Tree.Inorder1(current_Branch)
    elif choice == "2":
        name = input("Enter name of file to be opened: ")
        file = Tree.search(name, current_Branch)
        if file is None:
            print("File does not exist!")
        else:
            print(file.get_Data())
    elif choice == "3":
        name = input("Enter name of new file: ")
        Tree.insertion(name, current_Branch)

    elif choice == "4":
        name = input("Enter name of file to be deleted: ")
        Tree.deletion(name, current_Branch)
    elif choice == "5":
        name = input("Enter name of file to be edited: ")
        Tree.edit(name, current_Branch)
    elif choice == "6":
        for branch in branches:
            print(branch)
    elif choice == "7":
        Branch_Name = input("Enter name of new branch: ")
        if Branch_Name in branches:
            print("Branch already exists")
            continue
        branches.append(Branch_Name)
        Previous_Branch, current_Branch = current_Branch, Branch_Name
        Tree.New_Branch(current_Branch, Previous_Branch)
        
    elif choice == "8":
        Branch_Name = input("Enter name of branch to switch to: ")
        if Branch_Name not in branches:
              print("Branch doesn't exist")
        Previous_Branch, current_Branch = current_Branch, Branch_Name

    elif choice == "exit" or choice == "9":
        file = None
        Tree = None   
        print("Exiting...")
        break
    else:
        print("Invalid Input")
