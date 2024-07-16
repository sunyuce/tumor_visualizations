# SYC python learning
# 时间：2024/7/8 19:06
import re

def getparams(file_path1, file_path2, file_path3):
    unt_bce_dice_losses = []
    fpn_bce_dice_losses = []
    segnet_bce_dice_losses = []
    unt_IoU = []
    fpn_IoU = []
    segnet_IoU = []
    unt_Dice = []
    fpn_Dice = []
    segnet_Dice = []

    with open(file_path1, 'r') as file:
        lines = file.readlines()
        for line in lines:
            match1 = re.search(r'Bce_loss:(\d+\.\d+)', line)
            if match1:
                unt_bce_dice_losses.append(float(match1.group(1)))
            match2 = re.search(r'mIoU: (\d+\.\d+)', line)
            if match2:
                unt_IoU.append(float(match2.group(1)))
            match3 = re.search(r'Dice: (\d+\.\d+)', line)
            if match3:
                unt_Dice.append(float(match3.group(1)))
    with open(file_path2, 'r') as file:
        lines = file.readlines()
        for line in lines:
            match1 = re.search(r'Val Loss: (\d+\.\d+)', line)
            if match1:
                fpn_bce_dice_losses.append(float(match1.group(1)))
            match2 = re.search(r'mIoU: (\d+\.\d+)', line)
            if match2:
                fpn_IoU.append(float(match2.group(1)))
            match3 = re.search(r'Dice: (\d+\.\d+)', line)
            if match3:
                fpn_Dice.append(float(match3.group(1)))
    with open(file_path3, 'r') as file:
        lines = file.readlines()
        for line in lines:
            match1 = re.search(r'Val Loss: (\d+\.\d+)', line)
            if match1:
                segnet_bce_dice_losses.append(float(match1.group(1)))
            match2 = re.search(r'mIoU: (\d+\.\d+)', line)
            if match2:
                segnet_IoU.append(float(match2.group(1)))
            match3 = re.search(r'Dice: (\d+\.\d+)', line)
            if match3:
                segnet_Dice.append(float(match3.group(1)))

    print(f"unt_Val_loss:{unt_bce_dice_losses}")
    print(f"fpn_Val_loss:{fpn_bce_dice_losses}")
    print(f"segnet_Val_loss:{segnet_bce_dice_losses}")
    print(f"unt_mIoU:{unt_IoU}")
    print(f"fpn_mIoU:{fpn_IoU}")
    print(f"segnet_mIoU:{segnet_IoU}")
    print(f"unt_Dice:{unt_Dice}")
    print(f"fpn_Dice:{fpn_Dice}")
    print(f"segnet_Dice:{segnet_Dice}")

# 替换为你的txt文件路径
file_path1 = 'static/txt/unet.txt'
file_path2 = 'static/txt/fpn.txt'
file_path3 = 'static/txt/segnet.txt'
getparams(file_path1,file_path2,file_path3)
