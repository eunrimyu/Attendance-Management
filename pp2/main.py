import sys
import pygame
import serial
import os
from datetime import datetime, timedelta
from math import pi

screen_width = 1200
screen_height = 900
screen = pygame.display.set_mode((screen_width, screen_height))

ser = serial.Serial('com3', 9600)

grid_number = 4
grid_margin = 15
rect_width = 120 
rect_height = 90

sensor_count = 5    # 센서 갯수
sensor = ["sensor_" + str(i) for i in range(sensor_count)]  # 센서네임
attendance = [False] * sensor_count     # 출석 체크(True/False)
sit_state = [False] * sensor_count      # 앉았는지 체크(True/False)
stand_state = [False] * sensor_count    # 일어났는지 체크(True/False)
first_sit_time = [datetime(1, 1, 1, 0, 0, 0)] * sensor_count     # 처음 앉은 시간
recent_sit_time = [datetime(1, 1, 1, 0, 0, 0)] * sensor_count    # 마지막 앉은 시간
total_sit_time = [timedelta(0)] * sensor_count      # 앉은 총 시간
recent_stand_time = [datetime(1, 1, 1, 0, 0, 0)] * sensor_count  # 마지막 일어난 시간
total_stand_time = [timedelta(0)] * sensor_count    # 자리비운 총 시간
sit_count = [0] * sensor_count      # 앉은 횟수
stand_count = [0] * sensor_count    # 일어난 횟수
attendance_state = [0] * sensor_count     # 0 = 결석 / 1 = 출석 / 2 = 지각
tardiness = timedelta(minutes=10)    # 지각 기준

desk_count = 6
grid_desk_number = 2
grid_desk_margin = 15
rect_desk_width = 255
rect_desk_height = 45

sensor_data = []
sensor_status = [False] * sensor_count

student_list = []
student_id = []
student_name = []

def main():
    pygame.init()
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("메인 화면")

    # 입력한 시간 데이터 가져오기
    with open("data.txt", "r") as file:
        input_class = file.readline().strip()
        input_name = file.readline().strip()
        input_starttime = file.readline().strip()
        input_endtime = file.readline().strip()

    current_time = datetime.now()       # 현재 시간 
    current_date = datetime.now().date()# 현재 날짜

    start_datetime = datetime.strptime(input_starttime, "%H:%M:%S").time()
    start_time = datetime.combine(current_date, start_datetime)

    end_datetime = datetime.strptime(input_endtime, "%H:%M:%S").time()
    end_time = datetime.combine(current_date, end_datetime)


    with open("student.txt", 'r', encoding='utf-8') as file:
        for line in file:
            # 각 줄의 양쪽 공백 및 개행 문자를 제거하고 리스트에 추가
            student_list.append(line.strip())

    
    for student_info in student_list:
        # 학번과 이름을 공백을 기준으로 분리
        id, name = student_info.split(" ", 1)
        student_id.append(int(id))
        student_name.append(name)

    # 상명대 이미지
    img_smu1 = pygame.image.load("img/smu1.png")
    img_smu1_width = img_smu1.get_rect().size[0]
    img_smu1_height = img_smu1.get_rect().size[1]
    smu1_width = img_smu1_width/5
    smu1_height = img_smu1_height/5
    smu1 = pygame.transform.scale(img_smu1, (smu1_width,smu1_height))

    # 레이아웃
    layout1 = pygame.Rect([5, 100, 555, 30]) # 5 100 555 750
    layout1_1 = pygame.Rect([5, 135, 555, 750])
    layout2 = pygame.Rect([570, 100, 625, 30])
    layout2_1 = pygame.Rect([570, 135, 625, 750])

    # 버튼
    exit_button_rect = pygame.Rect((screen_width - 80), 0, 80, 80)
    start_button_rect = pygame.Rect(280, 50, 60, 30)
    stop_button_rect = pygame.Rect(280, 50, 60, 30)
    font_small_button = pygame.font.Font(None, 20)

    # 종료 후 마지막 데이터 계산을 한 번 실행하기 위한 것
    end_save = 0

    # 기본 배경
    screen.fill((255, 255, 255))    # 배경 색
    screen.blit(smu1,[0,0])         # 상명대 로고
    pygame.draw.rect(screen, (18,32,122), [80, 0, screen_width - 80, 80])   # 상단 바


    class_in_session = True
    sensor_in_action = True

    while class_in_session:
        current_time = datetime.now()       # 현재 시간
        current_date = datetime.now().date()# 현재 날짜

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:  # 마우스 왼쪽 버튼이 눌렸을 때
                # START 버튼
                if start_button_rect.collidepoint(event.pos) and current_time < start_time:
                    start_time = current_time
                    start_datetime = current_time.replace(microsecond=0).time()
                    pygame.draw.rect(screen, (18,32,122), [80, 0, screen_width - 80, 80])
                # STOP 버튼
                elif stop_button_rect.collidepoint(event.pos) and start_time <= current_time <= end_time:
                    end_time = current_time
                    end_datetime = current_time.replace(microsecond=0).time()
                    pygame.draw.rect(screen, (18,32,122), [80, 0, screen_width - 80, 80])
                    sensor_in_action = False
                # EXIT 버튼
                elif event.button == 1 and exit_button_rect.collidepoint(event.pos):
                    pygame.quit()
                    sys.exit()

        # 수업 정보 (상단바)
        font_class_information = pygame.font.Font(None, 50)
        class_information = font_class_information.render(f"{input_class} / {input_name}", 1, (255, 255, 255))
        screen.blit(class_information, (90, 15))

        # 수업 시간 (상단바)
        font_time_information = pygame.font.Font(None, 30)
        time_information = font_time_information.render(f"{start_datetime} ~ {end_datetime}", 1, (255, 255, 255))
        screen.blit(time_information, (90, 55))
        
        # 레이아웃
        font_layout = pygame.font.Font(None,40)

        pygame.draw.rect(screen, (227, 195, 250), layout1)
        seat_text = font_layout.render("Seat", True, (255, 255, 255))
        seat_rect = seat_text.get_rect(center=layout1.center)
        screen.blit(seat_text, seat_rect)

        pygame.draw.rect(screen, (227, 195, 250), layout1_1)
        
        pygame.draw.rect(screen, (90, 178, 239), layout2)
        time_text = font_layout.render("Time Table", True, (255, 255, 255))
        time_rect = time_text.get_rect(center=layout2.center)
        screen.blit(time_text, time_rect)

        pygame.draw.rect(screen, (90, 178, 239), layout2_1)

        # 나가기 버튼
        pygame.draw.rect(screen, (18, 32, 122), exit_button_rect)
        font_button = pygame.font.Font(None, 30)
        button_text = font_button.render("EXIT", 1, (0, 0, 0))
        button_rect = button_text.get_rect(center=exit_button_rect.center)
        screen.blit(button_text, button_rect)

        draw_data() # 내용

        pygame.display.flip()   # 화면 업데이트

        # 수업 전
        if current_time < start_time:
            # START 버튼
            pygame.draw.rect(screen, (18, 32, 122), start_button_rect)
            start_button_text = font_small_button.render("[START]", 1, (255, 255, 255))
            start_button_rect = start_button_text.get_rect(center=start_button_rect.center)
            screen.blit(start_button_text, start_button_rect)

            pygame.display.flip() # 화면 업데이트

        # 수업 중
        if sensor_in_action and start_time <= current_time <= end_time: 
            try:
                ser.flushInput()
                data = ser.readline().decode('utf-8').strip()
                print(data)

                now = datetime.now()    # 데이터 입력 시점의 현재 시간
                print(now)

                # 윈도우 아래에 데이터 입력 표시
                font = pygame.font.Font(None, 30)
                info_text = font.render(("data : " + data), 1, (0, 0, 255))
                screen.blit(info_text, (5, screen_height-25))

                sensor_data.append(f"{now} - {data}")

                # 데이터 처리
                sensor_id, event_type = data.split()
                sensor_number = int(sensor_id.split('_')[1])

                # 상태에 따라 색상 변경 및 센서별 데이터 저장
                if event_type == 'sit':
                    color = (0, 255, 0)  # 앉으면 녹색으로 변경
                    if not attendance[sensor_number]:
                        attendance[sensor_number] = True
                        attendance_state[sensor_number] += 1
                        first_sit_time[sensor_number] = now
                        if first_sit_time[sensor_number] >= start_time + tardiness: # 지각
                            attendance_state[sensor_number] += 1
                    sit_state[sensor_number] = True
                    stand_state[sensor_number] = False
                    recent_sit_time[sensor_number] = now
                    sit_count[sensor_number] += 1

                elif event_type == 'stand':
                    color = (255, 0, 0)   # 일어나면 빨간색으로 변경
                    sit_state[sensor_number] = False
                    stand_state[sensor_number] = True
                    recent_stand_time[sensor_number] = now
                    stand_count[sensor_number] += 1

                # 누적 시간 반영
                if sit_state[sensor_number] == False:
                    total_sit_time[sensor_number] += now - recent_sit_time[sensor_number]
                elif stand_state[sensor_number] == False and sit_count[sensor_number] > 1:
                    total_stand_time[sensor_number] += now - recent_stand_time[sensor_number]

                draw_data() # 내용

                # STOP 버튼
                pygame.draw.rect(screen, (18, 32, 122), stop_button_rect)
                stop_button_text = font_small_button.render("[STOP]", 1, (255, 255, 255))
                stop_button_rect = stop_button_text.get_rect(center=stop_button_rect.center)
                screen.blit(stop_button_text, stop_button_rect)

                pygame.display.flip()  # 화면 업데이트

            except UnicodeDecodeError as e:
                data = "Invalid UTF-8 Data"

        # 수업 후
        if end_time <= current_time and end_save == 0:
            print("=====")
            print(end_time)
            print(current_time)
            for i in range(sensor_count):
                if sit_state[i] == True:
                    print(recent_sit_time[i])
                    total_sit_time[i] += end_time - recent_sit_time[i]

                elif stand_state[i] == True:
                    print(recent_stand_time[i])
                    total_stand_time[i] += end_time - recent_stand_time[i]

                if total_sit_time[i] <= total_stand_time[i]:
                    attendance_state[i] = 0

            end_save += 1

        draw_data() # 내용

        pygame.display.flip()   # 화면 업데이트

    pygame.quit()
    return True

# 실시간 자리 : 사각형 그림
def draw_data():
    # 자리
    for i in range(sensor_count):
        row = i // grid_number
        col = i % grid_number
        x = col * (rect_width + grid_margin) + 20
        y = row * (rect_height + grid_margin*7) + 250
        if attendance[i]:
            if stand_state[i]:
                color = (255, 0, 0)
            else:
                color = (0, 255, 0)
        else:
            color = (134, 130, 127)
        draw_rectangle(screen, x, y, rect_width, rect_height, i, color)

    # 책상
    for i in range(desk_count):
        row = i // grid_desk_number
        col = i % grid_desk_number
        x = col * (rect_desk_width + grid_desk_margin) + 20
        y = row * (rect_desk_height +grid_desk_margin*10) + 200
        pygame.draw.rect(screen,(134, 130, 127),(x,y,rect_desk_width,rect_desk_height))

    font_data_table = pygame.font.Font(None, 22)
    draw_data_table(screen, font_data_table, sensor_data, 580, 155)

# 사각형 그림 안에 글자
def draw_rectangle(surface, x, y, width, height, sensor_number, color):
    # 학번 표시
    pygame.draw.rect(surface, color, (x, y, width, height))
    font = pygame.font.Font(None, 25)
    text = font.render(f"{student_id[sensor_number]}", 1, (0, 0, 0))
    text_rect = text.get_rect(center=(x + width // 2, y + height // 3))
    surface.blit(text, text_rect)
 
    # 이름 표시
    font_name_box = pygame.font.SysFont('malgungothic', 20)
    name_box_text = font_name_box.render(f"{student_name[sensor_number]}", 1, (0, 0, 0))
    name_box_rect = name_box_text.get_rect(center=(x + width // 2, y + height // 1.5))
    surface.blit(name_box_text, name_box_rect)
    

# 시간 데이터 표
def draw_data_table(surface, font, sensor_data, x, y): 

    row_height = 50 # 행 너비
    column_width = 97  # 열 너비
    header_text = font.render("ID & Name", 1, (0, 0, 0))
    surface.blit(header_text, (x, y))

    column1 = font.render("first sit", 1, (0, 0, 0))
    screen.blit(column1, (x + column_width, y))

    column2 = font.render("recent sit", 1, (0, 0, 0))
    screen.blit(column2, (x + 2 * column_width, y))

    column3 = font.render("recent stand", 1, (0, 0, 0))
    screen.blit(column3, (x + 3 * column_width, y))

    column4 = font.render("total sit", 1, (0, 0, 0))
    screen.blit(column4, (x + 4 * column_width, y))

    column5 = font.render("total stand", 1, (0, 0, 0))
    screen.blit(column5, (x + 5 * column_width, y))

    for i, sensor_number in enumerate(range(sensor_count)):
        additional_info_y = y + row_height
        horizontal_line_y = additional_info_y - 15
        vertical_line_x = x + column_width - 5
        vertical_line_y = y - 15

        # 가로 선
        pygame.draw.line(screen, (240, 248, 255), [x-5, horizontal_line_y + i * row_height], [x + 610, horizontal_line_y + i * row_height], 3)
        # 세로 선
        for j in range (0,6,1):
            pygame.draw.line(screen, (240, 248, 255), [vertical_line_x + j * column_width, vertical_line_y], [vertical_line_x + j * column_width, vertical_line_y + row_height * (sensor_count + 1)], 3)

        
        # 첫 번째 열 : sensor_number
        id_text = font.render(str(student_id[sensor_number]), 1, (0, 0, 0))
        surface.blit(id_text, (x, additional_info_y + i * row_height))

        font_name = pygame.font.SysFont('malgungothic', 13)
        name_text = font_name.render(str(student_name[sensor_number]), 1, (0, 0, 0))
        surface.blit(name_text, (x, additional_info_y + i * row_height + 10))

        # 나머지 열 : 시간 데이터
        first_sit_text = font.render(first_sit_time[sensor_number].strftime('%H:%M:%S'), 1, (0, 0, 0))
        surface.blit(first_sit_text, (x + column_width, additional_info_y + i * row_height))

        recent_sit_text = font.render(recent_sit_time[sensor_number].strftime('%H:%M:%S'), 1, (0, 0, 0))
        surface.blit(recent_sit_text, (x + 2 * column_width, additional_info_y + i * row_height))

        recent_stand_text = font.render(recent_stand_time[sensor_number].strftime('%H:%M:%S'), 1, (0, 0, 0))
        surface.blit(recent_stand_text, (x + 3 * column_width, additional_info_y + i * row_height))

        total_sit_text = font.render(str(total_sit_time[sensor_number].seconds // 3600).zfill(2) + ":" + str((total_sit_time[sensor_number].seconds // 60) % 60).zfill(2) + ":" + str(total_sit_time[sensor_number].seconds % 60).zfill(2), 1, (0, 0, 0))
        surface.blit(total_sit_text, (x + 4 * column_width, additional_info_y + i * row_height))

        total_stand_text = font.render(str(total_stand_time[sensor_number].seconds // 3600).zfill(2) + ":" + str((total_stand_time[sensor_number].seconds // 60) % 60).zfill(2) + ":" + str(total_stand_time[sensor_number].seconds % 60).zfill(2), 1, (0, 0, 0))
        surface.blit(total_stand_text, (x + 5 * column_width, additional_info_y + i * row_height))

        attendance_state_text = font.render(f"{attendance_state[sensor_number]}", 1, (0, 0, 0))
        surface.blit(attendance_state_text, (x + 6 * column_width, additional_info_y + i * row_height))

if __name__ == "__main__":
    main()
