import os
import subprocess
import re

# Tạo một đường dẫn mới
def create_folder():
    new_directory_path = "mgca/data/EndoDanhHuy"

    # Kiểm tra xem thư mục đã tồn tại chưa
    if not os.path.exists(new_directory_path):
        # Nếu thư mục chưa tồn tại, tạo thư mục mới
        os.makedirs(new_directory_path)
        print("Đã tạo thư mục thành công!")
    else:
        print("Thư mục đã tồn tại.")

    # tao thu muc chia data
    temp = ["train", "val", "test", "train_xml", "val_xml", "test_xml"]

    for i in temp:
        new_directory_path = f"mgca/data/EndoDanhHuy/{i}"

        # Kiểm tra xem thư mục đã tồn tại chưa
        if not os.path.exists(new_directory_path):
            # Nếu thư mục chưa tồn tại, tạo thư mục mới
            os.makedirs(new_directory_path)
            print("Đã tạo thư mục thành công!")
        else:
            print("Thư mục đã tồn tại.")

def copy_data():

    temp1 = ["jpg", "xml"]
    # temp2 = ["train", "val", "test", "train_xml", "val_xml", "test_xml"]
    temp2 = ["train", "val", "test"]
    for i in temp1:
        for j in temp2:

            pattern = re.compile(rf'.*\.{i}$')
            source_folder = f"../../AYT_data_new1/{j}"
            if i == "xml":
                j = j + "_" + i
            destination_folder = f"mgca/data/EndoDanhHuy/{j}"

            # Lặp qua tất cả các tệp trong thư mục nguồn
            for filename in os.listdir(source_folder):
                # Kiểm tra xem tệp có phù hợp với biểu thức chính quy không
                if pattern.match(filename):
                    # Tạo đường dẫn tệp nguồn và đích
                    source_file = os.path.join(source_folder, filename)
                    destination_file = os.path.join(destination_folder, filename)
                    try:
                        subprocess.run(["cp", "-r", source_file, destination_file])
                        print("Copied!")
                    except subprocess.CalledProcessError as e:
                        print(f"Command failed with return code {e.returncode}")

if __name__ == "__main__":
    create_folder()
    copy_data()
