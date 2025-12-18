class TreeNode:
    def __init__(self, key):
        self.key = key
        self.left = None
        self.right = None
        self.height = 1

class AVLTree:
    # Допоміжна функція для отримання висоти 
    def get_height(self, node):
        if not node:
            return 0
        return node.height

    # Отримання фактора балансу
    def get_balance(self, node):
        if not node:
            return 0
        return self.get_height(node.left) - self.get_height(node.right)

    # Правий поворот 
    def right_rotate(self, y):
        x = y.left
        T2 = x.right

        # Виконання повороту
        x.right = y
        y.left = T2

        # Оновлення висот
        y.height = 1 + max(self.get_height(y.left), self.get_height(y.right))
        x.height = 1 + max(self.get_height(x.left), self.get_height(x.right))

        return x

    # Лівий поворот 
    def left_rotate(self, x):
        y = x.right
        T2 = y.left

        # Виконання повороту
        y.left = x
        x.right = T2

        # Оновлення висот
        x.height = 1 + max(self.get_height(x.left), self.get_height(x.right))
        y.height = 1 + max(self.get_height(y.left), self.get_height(y.right))

        return y

    # Рекурсивна функція вставки [cite: 16, 19]
    def insert(self, node, key):
        # 1. Стандартна вставка BST
        if not node:
            return TreeNode(key)

        if key < node.key:
            node.left = self.insert(node.left, key)
        elif key > node.key:
            node.right = self.insert(node.right, key)
        else:
            return node  # Дублікати не додаємо

        # 2. Оновлення висоти поточного вузла
        node.height = 1 + max(self.get_height(node.left), self.get_height(node.right))

        # 3. Отримання балансу
        balance = self.get_balance(node)

        # 4. Балансування, якщо вузол став незбалансованим

        # Left Left Case
        if balance > 1 and key < node.left.key:
            return self.right_rotate(node)

        # Right Right Case
        if balance < -1 and key > node.right.key:
            return self.left_rotate(node)

        # Left Right Case
        if balance > 1 and key > node.left.key:
            node.left = self.left_rotate(node.left)
            return self.right_rotate(node)

        # Right Left Case
        if balance < -1 and key < node.right.key:
            node.right = self.right_rotate(node.right)
            return self.left_rotate(node)

        return node

    # Функція для красивого виводу дерева (Preorder)
    def pre_order(self, node):
        if not node:
            return
        print(f"{node.key} ", end="")
        self.pre_order(node.left)
        self.pre_order(node.right)

# Тестування
if __name__ == "__main__":
    tree = AVLTree()
    root = None

    # Вставка даних
    keys = [10, 20, 30, 40, 50, 25]
    print(f"Вставляємо: {keys}")
    
    for key in keys:
        root = tree.insert(root, key)

    # Вивід результату
    # Очікується збалансоване дерево, де корінь 30
    print("Pre-order traversal побудованого AVL-дерева:")
    tree.pre_order(root)
    print(f"\nКорінь дерева: {root.key}")
