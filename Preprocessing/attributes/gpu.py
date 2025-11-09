# gpu_utils.py
import pandas as pd
import re

def clean_gpu_name(gpu):
    """
    Chuẩn hóa tên GPU:
    - Viết thường
    - Thay dấu '-' thành khoảng trắng
    - Loại bỏ ký tự @, ™, ®, <br>, ...
    - Giữ nguyên các ký tự Unicode (để giữ 'lõi', 'nhân')
    - Bỏ khoảng trắng thừa
    """
    gpu = str(gpu).lower()
    gpu = gpu.replace("‑", " ")  # EN DASH → space
    gpu = gpu.replace("-", " ")  # ASCII dash → space               
    gpu = re.sub(r"<br>", " ", gpu)            # loại bỏ html <br>
    gpu = re.sub(r"[@™®]", "", gpu)            # loại bỏ ký tự đặc biệt
    gpu = re.sub(r"\s+", " ", gpu).strip()     # chuẩn hóa khoảng trắng
    return gpu

import re

def gpu_cores_label(gpu):
    """
    Nhận diện GPU dựa trên số lõi nếu không match High/Mid/Low.
    """
    if gpu is None or str(gpu).strip() == "":
        return None
    gpu_clean = str(gpu).lower()

    # Tìm số lõi
    match = re.search(r'(\d+)\s*(core|lõi|nhân|C)', gpu_clean)
    if match:
        cores = int(match.group(1))
        if cores >= 6:
            return "High"
        elif cores >= 4:
            return "Mid"
        else:
            return "Low"
    return None

def gpu_performance_bin(gpu):
    import pandas as pd
    if pd.isna(gpu) or str(gpu).strip() == "":
        return None

    gpu_clean = clean_gpu_name(gpu)

    # Nếu bạn muốn tự động sửa lỗi phổ biến:
    gpu_clean = gpu_clean.replace("mail g", "mali g")

    # Danh sách đầy đủ dựa trên GPU bạn cung cấp
    high_gpus = [
        "adreno 730","adreno 740","adreno 750","adreno 830",
        "mali g78","mali g710","mali g710 mc","mali g615",
        "mali g77 mp","mali g76 mp","immortalis","xclipse",
        "apple gpu","gpu 6 loi","gpu 5 loi","gpu 5 loi moi",
        "mali g76 mc","mali g72 mp","mali g77 mc","mali g72 mp18", "mali g72 mp3",
        "mali g76 mp10","mali g78 mp10","mali g78 mp14",
        "apple gpu 5 nhan","apple gpu 4 core","apple gpu 4 nhan","arm g615 mc6"
    ]
    mid_gpus = [
        "adreno 66","adreno 67","adreno 71","adreno 72",
        "adreno 644","adreno 642","adreno 642l","adreno 650",
        "adreno 619","adreno 618","adreno 612","adreno 610", "adreno 619", "adreno 620","adreno 630",
        "mali g68","mali g610","mali g57","mali g52","arm mali g57",
        "arm mali g72 mp3","arm g57","mali g51","powervr gm",
        "powervr8320","amd titan","mt676","img","adreno 670",
        "adreno 710","adreno 720","mali g57 mc2","mali g57 mc3",
        "mali g57 mc4","mali g52 mp2","mali g52 mp","arm mali g57 mp1","img"
    ]
    low_gpus = [
        "adreno 50","powervr ge","ge8320","ge8322","4 core gpu",
        "gpu 4 nhan","gpu 5 loi voi neural","gpu 6 loi voi neural",
        "4nm tsmc","null","ram","rom","sm a146b","sm a146p",
        "adreno 308","adreno 512","mali t720 mp2","powervr ge8100"
    ]

    # Check theo thứ tự ưu tiên
    if any(h in gpu_clean for h in high_gpus):
        return "High"
    if any(m in gpu_clean for m in mid_gpus):
        return "Mid"
    if any(l in gpu_clean for l in low_gpus):
        return "Low"
    
    # check số lõi nếu không match
    cores_label = gpu_cores_label(gpu_clean)
    if cores_label is not None:
        return cores_label
    
    return None


def process_gpu(df):
    """
    Tạo cột GPU_Performance dựa trên nhãn GPU.
    """
    gpu_col = next((c for c in df.columns if c.lower() in ["gpu_name","gpu", "GPU"]), None)
    if gpu_col is None:
        raise KeyError("DataFrame không có cột gpu/gpu_name.")

    df["gpu"] = df[gpu_col].apply(gpu_performance_bin)
    return df

# Ví dụ sử dụng
if __name__ == "__main__":
    data = {
        "gpu": [
            "Adreno 830",
            "GPU 4 lõi mới<br>Neural Engine 16 lõi mới",
            "Qualcomm® Adreno™ 618",
            " Mali-G52",
            "Mali-G52 2EEMC2",
            " 4 nhân 2.0 GHz & 4 nhân 1.8 GHz",
            "Mali-G76 MP18",
            "ARM Mali-G57 MP4",
            " Adreno 740",
            "Mali-G72 MP18",
            "Apple GPU 5 nhân",
            "5 nhân GPU",
            "Arm® Mali™ -G57 2cores, up to 950MHz",
            "Mali-G76 MP10",
            " Mali-G52 MC2",
            "Adreno 610@1050MHz",
            "RAM 48MB, ROM 128MB",
            "G57@4C 850MHz",
            " IMG PowerVR GE8322",
            "ARM Mali-G68",
            "Qualcomm® Adreno™ GPU",
            "4nm TSMC process"
        ]
    }
    df = pd.DataFrame(data)
    df = process_gpu(df)
    print(df)
