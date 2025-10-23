class MemoryBlock:
    def __init__(self, start, size, is_free=True, process_name="None"):
        self.start = start
        self.size = size
        self.is_free = is_free
        self.process_name = process_name
        self.next = None


class MemoryManager:
    def __init__(self, total_size):
        self.head = MemoryBlock(0, total_size, True, "None")

    def allocate(self, process_name, size):
        temp = self.head
        while temp:
            if temp.is_free and temp.size >= size:
                if temp.size > size:
                    new_block = MemoryBlock(temp.start + size, temp.size - size, True, "None")
                    new_block.next = temp.next
                    temp.next = new_block
                temp.size = size
                temp.is_free = False
                temp.process_name = process_name
                print(f"Allocated {size} units to {process_name}.")
                return
            temp = temp.next
        print(f"Memory allocation failed for {process_name} (requested {size} units).")

    def deallocate(self, process_name):
        temp = self.head
        while temp:
            if not temp.is_free and temp.process_name == process_name:
                temp.is_free = True
                temp.process_name = "None"
                print(f"Memory deallocated from {process_name}")
                self.merge_free_blocks()
                return
            temp = temp.next
        print(f"Process '{process_name}' not found!")

    def merge_free_blocks(self):
        temp = self.head
        while temp and temp.next:
            if temp.is_free and temp.next.is_free:
                temp.size += temp.next.size
                temp.next = temp.next.next
            else:
                temp = temp.next

    def display(self):
        print("\nMemory Layout:")
        print("-" * 20)
        temp = self.head
        while temp:
            end_address = temp.start + temp.size - 1
            status = "Free" if temp.is_free else f"Used by {temp.process_name}"
            print(f"[{temp.start:04} - {end_address:04}]  {status}")
            temp = temp.next
        print("-" * 20)


def main():
    print("==== Memory Management Simulator =====")
    while True:
        try:
            total_size = int(input("What's total size of memory? "))
            if total_size <= 0:
                print("[!] Please enter a number greater than 0.")
                continue
            break
        except ValueError:
            print("Invalid input. Please enter a valid integer.")

    manager = MemoryManager(total_size)

    while True:
        print("\nMenu:")
        print("1. Allocate Memory")
        print("2. Deallocate Memory")
        print("3. Display Memory Blocks")
        print("4. Exit")

        choice = input("Enter your choice: ")
        if choice == "1":
            process = input("Enter process name: ")
            while True:
                try:
                    size = int(input("Enter memory size to allocate: "))
                    if size <= 0:
                        print("[!] Please enter a number greater than 0.")
                        continue
                    break
                except ValueError:
                    print("Invalid input. Please enter a valid integer.")
            manager.allocate(process, size)

        elif choice == "2":
            process = input("Enter process name to deallocate: ")
            manager.deallocate(process)

        elif choice == "3":
            manager.display()

        elif choice == "4":
            print("Exiting simulator...")
            break

        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()