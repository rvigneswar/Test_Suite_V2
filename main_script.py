from selenium import webdriver
from selenium.webdriver.common.by import By
import os, time, paramiko, datetime


# check serial no length
def validate_serial_no(num):
    if len(num) == 15:
        return True
    else:
        return False


# login to UI
def login_to_ui():
    print("Login to UI with 192.168.4.1")
    driver.get("http://192.168.4.1")
    time.sleep(wait_time)
    driver.find_element(By.XPATH, '//*[@id="username-select"]').click()
    driver.find_element(By.XPATH, username).click()
    time.sleep(wait_time)
    driver.find_element(By.XPATH, '//*[@id="root"]/div/div/div/div/div/div[2]/form/div[2]/div/input').send_keys(
        password)
    time.sleep(wait_time)
    driver.find_element(By.XPATH, '//*[@id="root"]/div/div/div/div/div/div[2]/form/div[3]/div[2]/button').click()
    time.sleep(wait_time)


# Getting Dynamic IP
def get_dynamic_ip():
    print("Getting Dynamic IP from UI....")
    driver.find_element(By.XPATH,
                        '//*[@id="root"]/div/div/div[1]/nav/div[2]/div/div/div/div/div[2]/div/a[3]/button').click()
    driver.find_element(By.XPATH, '//*[@id="root"]/div/div/div[1]/main/div[1]/header/div/div/div/button[3]').click()
    time.sleep(wait_time)
    driver.find_element(By.XPATH,
                        '//*[@id="root"]/div/div/div[1]/main/div[1]/div/div[2]/div[1]/div[2]/button[1]').click()
    driver.implicitly_wait(2 + wait_time * 1000)
    url = driver.find_element(By.XPATH,
                              '//*[@id="root"]/div/div/div[1]/main/div[1]/div/div[2]/div[6]/div/input').get_attribute(
        "value")
    time.sleep(wait_time)
    print(f"The dynamic IP is : {url}.")
    return url


# Disk and Ram Usage
def check_disk_ram_usage(url, port, uname, passwd):
    print("Checking Disk Usage....")
    ssh.connect(url, port, uname, passwd)
    stdin1, stdout1, stderr1 = ssh.exec_command("df -h | grep /dev/disk/by-label/otaroot | awk '{print $3}'")
    disk_usage = stdout1.readline()
    print(f"{disk_usage.strip()} disk is being used.")
    print("Checking RAM Usage....")
    ssh.connect(url, port, uname, passwd)
    stdin2, stdout2, stderr2 = ssh.exec_command("free -mh | grep Mem | awk '{print $3}'")
    ram_usage = stdout2.readline()
    print(f"{ram_usage.strip()} RAM is being used.")
    return disk_usage.strip(), ram_usage.strip()


# CPU Temperature
def check_cpu_temp(url, port, uname, passwd):
    print("Checking CPU Temperature....")
    ssh.connect(url, port, uname, passwd)
    stdin3, stdout3, stderr3 = ssh.exec_command("cat /sys/class/thermal/thermal_zone0/temp")
    cpu_temp = stdout3.readline().split('\n')[0]
    print(f"The CPU temperature is {int(cpu_temp) / 1000} deg.")
    return int(cpu_temp) / 1000


# Bluetooth
def check_bluetooth(url, port, uname, passwd):
    print("Checking Bluetooth....")
    ssh.connect(url, port, uname, passwd)
    ssh.exec_command("bluetoothctl power on && timeout 15s bluetoothctl scan on")
    stdin4, stdout4, stderr4 = ssh.exec_command('dmesg | grep "Blue"')
    cmd_output = stdout4.readlines()
    if "Bluetooth" in cmd_output[0].strip():
        return True
    else:
        return False


# SD Card
def check_sd_card(url, port, uname, passwd):
    print("Checking SD Card....")
    ssh.connect(url, port, uname, passwd)
    stdin, stdout, stderr = ssh.exec_command("ls /dev/")
    output = stdout.readlines()
    for line in output:
        if "mmcblk1" in line.split('\n'):
            return True
    else:
        return False


# Login with dynamic IP
def login_dyn_ip(url):
    print(f"Login with Dynamic IP {url}")
    driver.switch_to.new_window("Tab")
    driver.get(f"http://{url}")
    time.sleep(wait_time)
    driver.find_element(By.XPATH, '//*[@id="username-select"]').click()
    driver.find_element(By.XPATH, username).click()
    time.sleep(wait_time)
    driver.find_element(By.XPATH, '//*[@id="root"]/div/div/div/div/div/div[2]/form/div[2]/div/input').send_keys(
        password)
    time.sleep(wait_time)
    driver.find_element(By.XPATH, '//*[@id="root"]/div/div/div/div/div/div[2]/form/div[3]/div[2]/button').click()
    time.sleep(wait_time)
    print("Login Successful....")


# Dashboard
def check_ui_navigation():
    print("Checking UI Navigation....")
    driver.find_element(By.XPATH,
                        '//*[@id="root"]/div/div/div[1]/nav/div[2]/div/div/div/div/div[2]/div/a[1]/button').click()
    zone_id = driver.find_element(By.XPATH, '//*[@id="root"]/div/div/div[1]/header/div/div[2]/div[1]/h6').text
    plant_id = driver.find_element(By.XPATH, '//*[@id="root"]/div/div/div[1]/header/div/div[2]/div[2]/h6').text
    time_stamp = driver.find_element(By.XPATH, '//*[@id="root"]/div/div/div[1]/header/div/div[3]/h6').text
    for i in range(2, 7):
        driver.find_element(By.XPATH, '//*[@id="root"]/div/div/div[1]/nav/div[2]/div/div/div/div/div[2]/div/a[' + str(
            i) + ']/button').click()
        time.sleep(wait_time + 2)
        if i == 4:
            driver.find_element(By.XPATH,
                                '//*[@id="root"]/div/div/div[1]/main/div[1]/div[2]/div/table/tbody/tr[1]/td[6]/span/span[1]/span[1]/input').click()
            time.sleep(wait_time)
            driver.find_element(By.XPATH,
                                '//*[@id="root"]/div/div/div[1]/main/div[1]/div[2]/div/table/tbody/tr[2]/td[6]/span/span[1]/span[1]/input').click()
            time.sleep(wait_time)
            driver.find_element(By.XPATH,
                                '//*[@id="root"]/div/div/div[1]/main/div[1]/div[2]/div/table/tbody/tr[3]/td[6]/span/span[1]/span[1]/input').click()
            time.sleep(wait_time)
        if i == 6:
            hardware_version = driver.find_element(By.XPATH,
                                                   '//*[@id="root"]/div/div/div[1]/main/div[1]/div/div[1]/code').text
            print(f"The hardware version is {hardware_version}.")
            software_version = driver.find_element(By.XPATH,
                                                   '//*[@id="root"]/div/div/div[1]/main/div[1]/div/div[2]/code').text
            print(f"The software version is {software_version}")
    driver.find_element(By.XPATH,
                        '//*[@id="root"]/div/div/div[1]/nav/div[2]/div/div/div/div/div[2]/div/a[1]/button').click()
    time.sleep(wait_time)
    wind_sensor = driver.find_element(By.XPATH,
                                      '//*[@id="root"]/div/div/div[1]/main/div[2]/div/div[2]/div[2]/div/div/div[2]/div[2]/h6').text
    time.sleep(wait_time)
    wind_direction = driver.find_element(By.XPATH,
                                         '//*[@id="root"]/div/div/div[1]/main/div[2]/div/div[2]/div[2]/div/div/div[2]/div[2]/h6').text
    time.sleep(wait_time)
    snow_sensor = driver.find_element(By.XPATH,
                                      '//*[@id="root"]/div/div/div[1]/main/div[2]/div/div[2]/div[3]/div/div/div[2]/div[2]/h6').text
    time.sleep(wait_time)
    flood_sensor = driver.find_element(By.XPATH,
                                       '//*[@id="root"]/div/div/div[1]/main/div[2]/div/div[2]/div[4]/div/div/div[2]/div[2]/h6').text
    time.sleep(2)
    time.sleep(wait_time)
    return wind_sensor, wind_direction, snow_sensor, flood_sensor, hardware_version, software_version


# Adding tracker
def add_tracker():
    print("Adding Tracker....")
    driver.find_element(By.XPATH,
                        '//*[@id="root"]/div/div/div[1]/nav/div[2]/div/div/div/div/div[2]/div/a[2]/button').click()
    driver.find_element(By.XPATH,
                        '//*[@id="root"]/div/div/div[1]/main/div[1]/header/div/div/div/div/div/button[2]').click()
    # input("Configure Row Controller with the required panID and press Enter....")
    while True:
        try:
            driver.find_element(By.XPATH,
                                '//*[@id="root"]/div/div/div[1]/main/div[1]/div/div[2]/div/div/div[2]/button[1]').click()
            time.sleep(wait_time)

            driver.find_element(By.XPATH,
                                '//*[@id="root"]/div/div/div[1]/main/div[1]/div/div[2]/div/div[2]/div[2]/table/tbody/tr/td[1]/span/span[1]/input').click()
            time.sleep(wait_time)

            driver.find_element(By.XPATH,
                                '//*[@id="root"]/div/div/div[1]/main/div[1]/div/div[2]/div/div[2]/div[1]/div[1]/p/button').click()
            time.sleep(wait_time)
            driver.find_element(By.XPATH,
                                '//*[@id="root"]/div/div/div[1]/main/div[1]/header/div/div/div/div/div/button[1]').click()
            print("Tracker added Successfully.")
            break
        except:
            driver.find_element(By.XPATH,
                                '//*[@id="root"]/div/div/div[1]/main/div[1]/div/div[2]/div/div/div[2]/button[1]').click()
            time.sleep(wait_time)
    driver.find_element(By.XPATH, '//*[@id="root"]/div/div/div[1]/main/div[1]/div/div[1]/div[1]/div/div/div/button[1]').click()
    time.sleep(wait_time)
    rc_did_no = driver.find_element(By.XPATH, '//*[@id="root"]/div/div/div[1]/main/div[1]/div/div[2]/div/div/table/tbody/tr/td[3]').text
    rc_ver = driver.find_element(By.XPATH, '//*[@id="root"]/div/div/div[1]/main/div[1]/div/div[2]/div/div/table/tbody/tr/td[4]').text
    rc_status = driver.find_element(By.XPATH, '//*[@id="root"]/div/div/div[1]/main/div[1]/div/div[2]/div/div/table/tbody/tr/td[5]').text
    rc_mode = driver.find_element(By.XPATH, '//*[@id="root"]/div/div/div[1]/main/div[1]/div/div[2]/div/div/table/tbody/tr/td[8]').text
    rc_batt_volt = driver.find_element(By.XPATH, '//*[@id="root"]/div/div/div[1]/main/div[1]/div/div[2]/div/div/table/tbody/tr/td[11]/p/div/span[1]').text
    rc_batt_cur = driver.find_element(By.XPATH, '//*[@id="root"]/div/div/div[1]/main/div[1]/div/div[2]/div/div/table/tbody/tr/td[12]/div/span[1]').text
    rc_pv_volt = driver.find_element(By.XPATH, '//*[@id="root"]/div/div/div[1]/main/div[1]/div/div[2]/div/div/table/tbody/tr/td[9]/p/div/span[1]').text
    rc_pv_cur = driver.find_element(By.XPATH, '//*[@id="root"]/div/div/div[1]/main/div[1]/div/div[2]/div/div/table/tbody/tr/td[10]/p/div/span[1]').text
    return rc_did_no, rc_ver, rc_status, rc_mode, rc_batt_volt, rc_batt_cur, rc_pv_volt, rc_pv_cur


# NTP Sync
def check_ntp_sync():
    print("Checking NTP Sync....")
    driver.find_element(By.XPATH,
                        '//*[@id="root"]/div/div/div[1]/nav/div[2]/div/div/div/div/div[2]/div/a[3]/button').click()
    driver.implicitly_wait(wait_time * 1000)
    driver.find_element(By.XPATH, '//*[@id="root"]/div/div/div[1]/main/div[1]/header/div/div/div/button[5]').click()
    time.sleep(wait_time)
    driver.find_element(By.XPATH, '//*[@id="mui-component-select-timezone"]').click()
    driver.implicitly_wait(wait_time)
    t_zone = driver.find_element(By.XPATH, '//*[@id="menu-timezone"]/div[3]/ul/li[196]')
    driver.implicitly_wait(wait_time)
    time_zone_id_1 = t_zone.text
    t_zone.click()
    driver.find_element(By.XPATH, '//*[@id="root"]/div/div/div[1]/main/div[1]/div/div/div/button').click()
    driver.implicitly_wait(wait_time + 7 * 1000)
    driver.find_element(By.XPATH, '/html/body/div[3]/div[3]/div/div/div/div[2]/div/button[2]').click()
    time_zone_1 = driver.find_element(By.XPATH, '//*[@id="root"]/div/div[1]/div[1]/header/div/div[3]').get_attribute(
        "title")
    driver.find_element(By.XPATH, '//*[@id="mui-component-select-timezone"]').click()
    driver.implicitly_wait(wait_time)
    t_zone_2 = driver.find_element(By.XPATH, '//*[@id="menu-timezone"]/div[3]/ul/li[197]')
    driver.implicitly_wait(wait_time)
    time_zone_id_2 = t_zone_2.text
    t_zone_2.click()
    driver.find_element(By.XPATH, '//*[@id="root"]/div/div/div[1]/main/div[1]/div/div/div/button').click()
    driver.implicitly_wait(wait_time + 7 * 1000)
    driver.find_element(By.XPATH, '/html/body/div[3]/div[3]/div/div/div/div[2]/div/button[2]').click()
    time.sleep(5)
    time_zone_2 = driver.find_element(By.XPATH,
                                      '//*[@id="root"]/div/div[1]/div[1]/header/div/div[3]').get_attribute("title")
    print(f"Test 1:\t\tTime Zone selected is {time_zone_id_1} and time synced is {time_zone_1}.")
    print(f"Test 2:\t\tTime Zone selected is {time_zone_id_2} and time synced is {time_zone_2}.")
    return time_zone_id_1, time_zone_1, time_zone_id_2, time_zone_2


# Board Temperature
def check_board_temp():
    driver.find_element(By.XPATH,
                        '//*[@id="root"]/div/div/div[1]/nav/div[2]/div/div/div/div/div[2]/div/a[3]/button').click()
    driver.implicitly_wait(wait_time * 3000)
    driver.find_element(By.XPATH, '//*[@id="root"]/div/div/div[1]/main/div[1]/header/div/div/div/button[7]').click()
    driver.implicitly_wait(wait_time * 3000)
    driver.find_element(By.XPATH,
                        '//*[@id="root"]/div/div/div[1]/main/div[1]/div/div[1]/div/div/div/div/button[2]').click()
    driver.implicitly_wait(wait_time * 3000)
    board_temp = driver.find_element(By.XPATH,
                                     '//*[@id="root"]/div/div/div[1]/main/div[1]/div/div[2]/div/div[2]/div[3]/div/div[2]/h2').text
    print(f"Board Temperature is {board_temp} deg.")
    return board_temp


# Writing to file
def write_to_file(serial_no, url, disk, ram, data, rc_data, ntp_data, board_temp, bluetooth, sd_card):
    file = open(f"Report_{serial_no}.txt", "a")
    now = datetime.datetime.now()
    file.write(str(now.strftime("%Y-%m-%d %H:%M:%S")))
    file.write("\t")
    file.write(f"Serial No: {serial_no}.")
    file.write("\n")
    file.write("\n")
    file.write(f"Dynamic IP: {url}.")
    file.write("\n")
    file.write(f"Disk Usage: {disk}.")
    file.write("\n")
    file.write(f"RAM Usage: {ram}.")
    file.write("\n")
    file.write(f"Board Temperature: {board_temp} deg.")
    file.write("\n")
    if bluetooth:
        file.write("Bluetooth is available.")
    else:
        file.write("Bluetooth is not available.")
    file.write("\n")
    if sd_card:
        file.write("SD_Card is available.")
    else:
        file.write("SD Card is not available.")
    file.write("\n")
    file.write("\n")
    file.write(f"Test for NTP Sync.")
    file.write("\n")
    file.write("Test 1:\t\t")
    file.write(f"Time Zone selected is {ntp_data[0]} and time is {ntp_data[1]}.")
    file.write("\n")
    file.write("Test 2:\t\t")
    file.write(f"Time Zone selected is {ntp_data[2]} and time is {ntp_data[3]}.")
    file.write("\n")
    file.write("\n")
    file.write(f"Tracker Data.")
    file.write("\n")
    file.write(f"RC DID NO: {rc_data[0]}.")
    file.write("\n")
    file.write(f"RC Version: {rc_data[1]}.")
    file.write("\n")
    file.write(f"RC Status: {rc_data[2]}.")
    file.write("\n")
    file.write(f"RC Mode: {rc_data[3]}.")
    file.write("\n")
    file.write(f"RC Battery Voltage: {rc_data[4]} volts.")
    file.write("\n")
    file.write(f"RC Battery Current: {rc_data[5]} amps.")
    file.write("\n")
    file.write(f"RC PV Voltage: {rc_data[6]} volts.")
    file.write("\n")
    file.write(f"RC PV Current: {rc_data[7]} amps.")
    file.write("\n")
    file.write("\n")
    file.write(f"Sensor data")
    file.write(f"Wind Speed: {data[0]} m/s.")
    file.write("\n")
    file.write(f"Wind Direction: {data[1]} deg.")
    file.write("\n")
    file.write(f"Snow Level: {data[2]} mm.")
    file.write("\n")
    file.write(f"Flood Level: {data[3]} mm.")
    file.write("\n")
    file.write(f"Hardware Version: {data[4]}.")
    file.write("\n")
    file.write(f"Software Version: {data[5]}.")



username = '//*[@id="menu-username"]/div[3]/ul/li[1]'
password = 'Admin'
uname = "torizon"
passwd = "sunshine"
port = 22
wait_time = 5
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
os_type = os.name
if os_type == "nt":
    driver_path = str(os.getcwd()) + "/driver/chromedriver.exe"
elif os_type == "posix":
    driver_path = str(os.getcwd()) + "/driver/chromedriver"

# inp = input("Press 'Enter' to continue(Press 'q' to exit)")
while True:
    serial_no = input("Enter the Serial Number: ")
    if validate_serial_no(serial_no):
        driver = webdriver.Chrome(executable_path=driver_path)
        driver.maximize_window()
        # main_addr = "172.16.0.3"
        login_to_ui()
        url = get_dynamic_ip()
        disk, ram = check_disk_ram_usage(url, port, uname, passwd)
        cpu_temp = check_cpu_temp(url, port, uname, passwd)
        bluetooth = check_bluetooth(url, port, uname, passwd)
        sd_card = check_sd_card(url, port, uname, passwd)
        login_dyn_ip(url)
        data = check_ui_navigation()
        rc_data = add_tracker()
        ntp_data = check_ntp_sync()
        board_temp = check_board_temp()
        write_to_file(serial_no, url, disk, ram, data, rc_data, ntp_data, board_temp, bluetooth, sd_card)
        driver.quit()
        break
    else:
        print("Please enter a valid serial number....")
