# This is a sample Python script.
from getpass import getpass

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

import psycopg2

# Press the green button in the gutter to run the script.

# 모드 선택
def mode_set():
    print("모드 선택")
    print("1. 인간 모드 "
          "2. 개발자 모드 "
          "3. 게임 종료")
    mod = int(input())
    if mod == 1:
        print("인간 모드로 접속합니다")
    elif mod == 2:
        print("개발자 모드로 접속합니다")
    else:
        print("게임 종료")
    return mod


# 개발자 모드 진입
def developer_mod():
    developer_id = get_developer_id()
    if not developer_id:
        create_developer()
    cursor.execute('''
             UPDATE developer
             SET login_state = 1
         ''')
    con.commit()
    while True:
        print("\nDeveloper Mode:")
        print("1: 몬스터 생성")
        print("2: 몬스터 정보 확인")
        print("3: 몬스터 제거")
        print("4: 아이템 생성")
        print("5: 아이템 제거")
        print("6: 티어 추가")
        print("7: 티어 제거")
        print("8: 종료")
        dev_choice = input("Select an option: ")

        if dev_choice == '1':
            create_monster()
        elif dev_choice == '2':
            view_monster_info()
        elif dev_choice == '3':
            remove_monster()
        elif dev_choice == '4':
            create_item()
        elif dev_choice == '5':
            remove_item()
        elif dev_choice == '6':
            add_rank()
        elif dev_choice == '7':
            remove_rank()
        elif dev_choice == '8':
            print("개발자 모드 종료")
            cursor.execute('''
                           UPDATE developer
                           SET login_state = 0
                       ''')
            con.commit()
            break
        else:
            print("잘못된 입력입니다. 다시 입력하세요")


# 개발자 ID 가져오기
def get_developer_id():
    cursor.execute('SELECT id FROM developer')
    developer_id = cursor.fetchone()
    return developer_id[0] if developer_id else None


# 개발자 ID 생성
def create_developer():
    cursor.execute('''
        INSERT INTO developer (id, login_state) 
        VALUES ('0', 1)
    ''')
    cursor.execute('''
        INSERT INTO game_account (id, name, password)
        VALUES ('0', 'developer', '0')
    ''')
    con.commit()


# 몬스터 생성
monster_id_counter = 0


def create_monster():
    global monster_id_counter

    # 개발자가 지정한 몬스터 정보를 가져오기
    cursor.execute('SELECT * FROM monster')
    monster_data = cursor.fetchall()

    if not monster_data:
        print("생성가능한 몬스터가 없습니다.")
        return

    # 개발자가 지정하는 몬스터와 개수 입력
    print("1: 좀비 2: 거미 3: 크리퍼 4: 스켈레톤 5: 피그좀비 6: 드래곤")
    monster_type = int(input("생성할 몬스터 번호를 선택하세요: "))
    num_monsters = int(input("생성할 몬스터의 갯수를 고르세요: "))

    for _ in range(num_monsters):
        # 각 몬스터에 대해 순차적으로 증가하는 ID 생성
        monster_id = generate_unique_monster_id(monster_type)

        # 개발자가 생성하는 몬스터 정보
        monster_name = monster_data[monster_type - 1][0]
        attack = int(monster_data[monster_type - 1][1])
        hp = int(monster_data[monster_type - 1][2])
        reward_exp = int(monster_data[monster_type - 1][3])
        reward_money = int(monster_data[monster_type - 1][4])

        print(monster_id)
        print(monster_name)
        print(attack)
        print(hp)
        print(reward_exp)
        print(reward_money)

        # Created_monster 테이블에 몬스터 추가

        cursor.execute('''
            INSERT INTO created_monster (monster_id, monster_name, attack, hp, reward_exp, reward_money)
            VALUES (%s, %s, %s, %s, %s, %s)
        ''', (monster_id, monster_name, attack, hp, reward_exp, reward_money))

    con.commit()
    print(f"몬스터 {num_monsters}마리 생성완료!")


def generate_unique_monster_id(monster_type):
    global monster_id_counter

    while True:
        # 각 몬스터에 대해 순차적으로 증가하는 ID 생성
        monster_id_counter += 1
        monster_id = f"{monster_type:02d}{monster_id_counter:05d}"

        # 이미 존재하는 몬스터 ID이면 계속 시도
        cursor.execute('SELECT COUNT(*) FROM created_monster WHERE monster_id = %s', (monster_id,))
        if cursor.fetchone()[0] == 0:
            break

    return str(monster_id)


# 몬스터 정보 확인
def view_monster_info():
    cursor.execute('''
        SELECT * FROM Monster
    ''')
    monsters = cursor.fetchall()

    if monsters:
        print("\n몬스터 정보:")
        print('{:<15}{:<15}{:<15}{:<15}{:<15}'.format("Name", "Attack", "HP", "Reward EXP", "Reward Money"))
        for monster in monsters:
            print('{:<15}{:<15}{:<15}{:<15}{:<15}'.format(monster[0], monster[1], monster[2], monster[3], monster[4]))
    else:
        print("No monsters found.")


# 몬스터 제거
def remove_monster():
    cursor.execute('''
            SELECT monster_id, monster_name FROM created_monster
        ''')
    monster_info = cursor.fetchall()

    if not monster_info:
        print("생성된 몬스터가 없습니다.")
        return

    print("Created Monsters:")
    for mons_id, mons_name in monster_info:
        print(f"ID: {mons_id}, Name: {mons_name}")

    monster_id = input("제거할 몬스터의 id를 입력하세요: ")
    # 입력한 ID에 해당하는 몬스터가 있는지 확인
    cursor.execute('''
        SELECT 1 FROM created_monster
        WHERE monster_id = %s
    ''', (monster_id,))
    exists = cursor.fetchone()

    if exists:
        cursor.execute('''
            DELETE FROM created_monster
            WHERE monster_id = %s
        ''', (monster_id,))
        con.commit()
        print("몬스터 제거 성공!")
    else:
        print("실패! 해당 ID에 해당하는 몬스터가 없습니다.")


# 아이템 생성
def create_item():
    item_name = input("생성할 아이템 이름 입력: ")
    item_type = input("생성할 아이템 종류 입력(Weapon or Potion): ")

    if item_type.lower() == 'weapon':
        attack = int(input("무기 공격력 입력: "))
        price = int(input("무기 가격 입력: "))
        durability = int(input("무기 내구도 입력: "))

        cursor.execute('''
                           INSERT INTO item_shop (item_name, item_type)
                           VALUES (%s, %s)
                       ''', (item_name, item_type))

        cursor.execute('''
            INSERT INTO weapon (weapon_name, attack, price, durability)
            VALUES (%s, %s, %s, %s)
        ''', (item_name, attack, price, durability))

        print("아이템 생성 완료!")

    elif item_type.lower() == 'potion':
        price = int(input("물약 가격 입력: "))
        heal = int(input("물약 회복력 입력: "))

        cursor.execute('''
                        INSERT INTO item_shop (item_name, item_type)
                        VALUES (%s, %s)
                    ''', (item_name, item_type))

        cursor.execute('''
            INSERT INTO potion (potion_name, price, heal)
            VALUES (%s, %s, %s)
        ''', (item_name, price, heal))

        print("아이템 생성 완료!")

    else:
        print("Invalid item type. Please enter 'Weapon' or 'Potion'.")

    con.commit()


def remove_item():
    cursor.execute('''
        SELECT item_name, item_type FROM item_shop
    ''')
    items = cursor.fetchall()

    if not items:
        print("현재 등록된 아이템이 없습니다.")
        return

    print("현재 등록된 아이템 목록:")
    for item_name, item_type in items:
        print(f"{item_name} - {item_type}")

    item_name = input("제거할 아이템 이름 입력: ")
    success = 0
    cursor.execute('''
        SELECT item_type FROM item_shop
        WHERE LOWER(item_name) = LOWER(TRIM(%s))
    ''', (item_name,))

    if not cursor.fetchone():
        print("등록된 아이템이 없습니다.")
        return

    item_type = cursor.fetchone()[0]

    if item_type == 'weapon':
        cursor.execute('''
                 DELETE FROM weapon
                 WHERE LOWER(weapon_name) = LOWER(TRIM(%s))
             ''', (item_name,))
        cursor.execute('''
            DELETE FROM item_shop
            WHERE LOWER(item_name) = LOWER(TRIM(%s))
        ''', (item_name,))

        success = 1
    elif item_type == "potion":
        cursor.execute('''
                   DELETE FROM potion
                   WHERE LOWER(potion_name) = LOWER(TRIM(%s))
               ''', (item_name,))
        cursor.execute('''
            DELETE FROM item_shop
            WHERE LOWER(item_name) = LOWER(TRIM(%s))
        ''', (item_name,))

        success = 1

    con.commit()

    if success == 1:
        print(f"{item_name} 아이템 제거 완료!")
    else:
        print(f"{item_name} 아이템을 찾을 수 없습니다.")


# 티어 추가
def add_rank():
    rank_name = input("생성할 티어 이름 입력: ")
    required_exp = int(input("필요한 경험치 입력: "))

    cursor.execute('''
        INSERT INTO rank (rank, exp)
        VALUES (%s, %s)
    ''', (rank_name, required_exp))

    con.commit()
    print("티어 생성 완료!")


# 티어 제거
def remove_rank():
    # 현재 등록된 티어 목록 보여주기
    cursor.execute('''
            SELECT rank FROM rank
        ''')
    ranks = cursor.fetchall()

    if not ranks:
        print("현재 등록된 티어가 없습니다.")
        return

    print("현재 등록된 티어 목록:")
    for rank in ranks:
        print(rank[0])

    rank_name = input("제거할 티어 이름 입력: ")

    # 제거하려는 티어가 티어 테이블에 있는지 확인
    cursor.execute('''
           SELECT COUNT(*) FROM rank
           WHERE rank = %s
       ''', (rank_name,))
    exists = cursor.fetchone()[0]

    if not exists:
        print(f"티어 '{rank_name}'가 존재하지 않습니다.")
    else:
        cursor.execute('''
               DELETE FROM rank
               WHERE rank = %s
           ''', (rank_name,))
        print(f"티어 '{rank_name}'를 제거하였습니다.")

    con.commit()



# 게임 실행

def run_game():
    logged_in = False
    human_id = None

    while True:
        if not logged_in:
            print("\n1: 회원가입\n2: 로그인\n3: 종료")
        else:
            print_menu()

        choice = input("선택: ")

        if not logged_in:
            if choice == '1':
                sign_up()
            elif choice == '2':
                human_id = log_in()
                logged_in = human_id is not False
            elif choice == '3':
                print("게임 종료!")
                break
            else:
                print("잘못된 입력입니다. 다시 입력하세요.")
        else:
            if choice == '1':
                view_account_state()
            elif choice == '2':
                view_human_state(human_id)
            elif choice == '3':
                print("로그아웃 되었습니다.")
                logged_in = False
                human_id = None
            elif choice == '4':
                view_created_monsters()
            elif choice == '5':
                assign_attack_target(human_id)
            elif choice == '6':
                attack_monster(human_id)
            elif choice == '7':
                view_inventory_items(human_id)
            elif choice == '8':
                view_inventory_weapons(human_id)
            elif choice == '9':
                view_inventory_potions(human_id)
            elif choice == '10':
                equip_weapon(human_id)
            elif choice == '11':
                unequip_weapon(human_id)
            elif choice == '12':
                consume_potion(human_id)
            elif choice == '13':
                view_shop()
            elif choice == '14':
                purchase_item(human_id)
            else:
                print("잘못된 입력입니다. 다시 입력하세요.")


def print_menu():
    print("--- 계정 ---")
    print("1. 계정 상태 보기")
    print("2. 캐릭터 상태 보기")
    print("3. 로그아웃")
    print("--- 몬스터 ---")
    print("4. 생성된 몬스터 보기")
    print("5. 공격할 몬스터 지정")
    print("6. 몬스터 공격")
    print("--- 인벤토리 ---")
    print("7. 인벤토리 아이템 정보 보기")
    print("8. 인벤토리 무기 정보 보기")
    print("9. 인벤토리 물약 정보 보기")
    print("10. 무기 장착")
    print("11. 무기 해제")
    print("12. 물약 섭취")
    print("--- 상점 ---")
    print("13. 상점 보기")
    print("14. 아이템 구입")


# 회원가입
def sign_up():
    print("회원가입")

    while True:
        new_id = input("ID: ")

        # 아이디 중복 확인
        cursor.execute('''
            SELECT id
            FROM game_account
            WHERE id = %s
        ''', (new_id,))
        existing_id = cursor.fetchone()

        if existing_id:
            print("이미 사용 중인 아이디입니다. 다른 아이디를 입력해주세요.")
        else:
            break

    password = input("password: ")
    name = input("이름: ")

    cursor.execute('''
        INSERT INTO game_account (id, name, password)
        VALUES (%s, %s, %s)
    ''', (new_id, name, password))

    cursor.execute('''
        INSERT INTO human (human_id, human_name, attack, hp, exp, money, equipped_weapon_id, rank)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    ''', (new_id, name, 2, 100, 0, 0, None, None))

    con.commit()
    print("회원가입 완료!")



# 로그인
def log_in():
    print("로그인")
    log_id = input("ID: ")
    password = input("password: ")

    cursor.execute('''
        SELECT * FROM game_account WHERE id = %s AND password = %s
    ''', (log_id, password))

    account = cursor.fetchone()

    if account:
        print("로그인 성공!")
        return account[0]
    else:
        print("로그인 실패! ID와 비밀번호를 다시 확인하세요.")
        return False


# 계정 상태 보기
def view_account_state():
    cursor.execute('''
        SELECT * FROM game_account
    ''')

    account_infos = cursor.fetchall()

    if account_infos:
        for account_info in account_infos:
            print("\n계정 상태:")
            print(f"ID: {account_info[0]}")
            print(f"이름: {account_info[1]}")
    else:
        print("계정을 찾을 수 없습니다.")


# 캐릭터 상태 보기
def view_human_state(human_id):
    cursor.execute('''
        SELECT * FROM human WHERE human_id = %s
    ''', (human_id,))

    character_info = cursor.fetchone()

    if character_info:
        print("\n--- 캐릭터 상태 ---")
        print(f"ID: {character_info[0]}")
        print(f"이름: {character_info[1]}")
        print(f"공격력: {character_info[2]}")
        print(f"체력: {character_info[3]}")
        print(f"경험치: {character_info[4]}")
        print(f"돈: {character_info[5]}")
        print(f"장착된 무기: {character_info[6]}")
        print(f"티어: {character_info[7]}")
    else:
        print("캐릭터 정보를 찾을 수 없습니다.")


# 생성된 몬스터 보기
def view_created_monsters():
    cursor.execute('''
            SELECT * FROM created_monster
        ''')
    monsters = cursor.fetchall()

    if monsters:
        print("\n--- 생성된 몬스터 ---")
        print("ID\tName\tAttack\tHP\tReward EXP\tReward Money")
        for monster in monsters:
            print(f"{monster[0]}\t{monster[1]}\t{monster[2]}\t{monster[3]}\t{monster[4]}\t{monster[5]}")
    else:
        print("생성된 몬스터가 없습니다.")


# 공격할 몬스터 지정
def assign_attack_target(human_id):

    monster_id = str(input("공격할 몬스터의 ID를 입력하세요: "))

    # 이미 다른 사용자가 monster_attack에 등록한 몬스터인지 검사
    cursor.execute('''
            SELECT COUNT(*)
            FROM monster_attack
            WHERE monster_id = %s
        ''', (monster_id,))

    if cursor.fetchone()[0] > 0:
        print("이미 공격받고있는 몬스터입니다. 다른 몬스터를 선택하세요.")
        return

    cursor.execute('''
            SELECT COUNT(*)
            FROM created_monster
            WHERE monster_id = %s
        ''', (monster_id,))

    if cursor.fetchone()[0] == 0:
        print("입력한 몬스터 ID가 유효하지 않습니다.")
        return

    # 인간이 몬스터를 공격 중인 경우, 먼저 기존의 몬스터 정보를 초기화
    cursor.execute('''
            DELETE FROM monster_attack
            WHERE human_id = %s
        ''', (human_id,))

    # 선택한 몬스터를 인간이 공격 중인 몬스터로 설정
    cursor.execute('''
           INSERT INTO monster_attack (monster_id, human_id)
           VALUES (%s, %s)
       ''', (monster_id, human_id))

    con.commit()
    print("목표 몬스터가 지정되었습니다.")


# 몬스터 공격
def attack_monster(human_id):
    # 인간이 현재 지정한 몬스터 정보 가져오기

    # monster_attack_info라는 view활용
    cursor.execute('''
        SELECT * FROM monster_attack_info WHERE human_id = %s
    ''', (human_id,))
    info = cursor.fetchone()

    if not info:
        print("지정된 몬스터가 없습니다.")
        return

    monster_id, monster_name, monster_attack, monster_hp, reward_exp, reward_money, human_attack, human_hp, human_exp, human_money, weapon_durability, equipped_weapon_id, h_id = info

    # 몬스터 공격
    if equipped_weapon_id and weapon_durability > 0:
        # 무기가 장착되어 있고 내구도가 0보다 큰 경우에만 무기의 내구도를 감소시킴
        weapon_durability -= 1
        cursor.execute('''
            UPDATE human_weapon
            SET durability = %s
            WHERE weapon_id = %s
        ''', (weapon_durability, equipped_weapon_id))

    human_damage = human_attack
    monster_hp -= human_damage

    cursor.execute('''
        UPDATE created_monster
        SET hp = %s
        WHERE monster_id = %s
    ''', (monster_hp, monster_id))

    if weapon_durability == 0 and equipped_weapon_id:
        # 무기 내구도가 0이 되면 무기를 해제하고 inventory에 추가
        cursor.execute('''
            DELETE FROM human_weapon
            WHERE weapon_id = %s
        ''', (equipped_weapon_id,))

        cursor.execute('''
            DELETE FROM inventory
            WHERE human_id = %s AND item_id = %s
        ''', (human_id, equipped_weapon_id))
        cursor.execute('''
            UPDATE human
            SET equipped_weapon_id = NULL
            WHERE human_id = %s
        ''', (human_id,))

    if monster_hp <= 0:
        # 몬스터를 성공적으로 처치한 경우
        print(f"{monster_name}을(를) 성공적으로 처치했습니다!")
        # 몬스터 공격 정보 삭제
        cursor.execute('''
            DELETE FROM monster_attack
            WHERE monster_id = %s
        ''', (monster_id,))
        # 몬스터 정보 삭제
        cursor.execute('''
            DELETE FROM created_monster
            WHERE monster_id = %s
        ''', (monster_id,))
        # 인간의 경험치 및 돈 증가
        new_exp = int(human_exp) + int(reward_exp)
        new_money = int(human_money) + int(reward_money)

        # 인간의 승급 여부 확인 및 처리
        check_and_promote(human_id, new_exp)

        cursor.execute('''
            UPDATE human
            SET exp = %s, money = %s
            WHERE human_id = %s
        ''', (new_exp, new_money, human_id))

    else:
        # 몬스터에게 공격을 받은 경우
        monster_damage = monster_attack
        human_hp -= monster_damage

        cursor.execute('''
            UPDATE human
            SET hp = %s
            WHERE human_id = %s
        ''', (human_hp, human_id))

        if human_hp <= 0:
            # 인간이 사망한 경우
            print("인간이 사망했습니다. 로그아웃 하세요.")
            # 인간 정보 초기화
            cursor.execute('''
                DELETE FROM human
                WHERE human_id = %s
            ''', (human_id,))
            # 게임 계정 삭제
            cursor.execute('''
                DELETE FROM game_account
                WHERE id = %s
            ''', (human_id,))
            # 게임 로그아웃
            cursor.execute('''
                DELETE FROM monster_attack
                WHERE human_id = %s
            ''', (human_id,))

        else:
            # 몬스터와 인간이 계속 전투 중인 경우
            print(f"{monster_name}에게 {human_damage}의 데미지를 입히고, {monster_name}에게 {monster_damage}의 데미지를 받았습니다.")
            # 몬스터와 인간의 현재 상태 출력
            print(f"인간 HP: {human_hp}, 몬스터 HP: {monster_hp}")

    con.commit()


# 자동 승급
def check_and_promote(human_id, new_exp):
    # 현재 경험치 및 랭크 가져오기
    cursor.execute('''
        SELECT exp, rank
        FROM human
        WHERE human_id = %s
    ''', (human_id,))
    current_exp, current_rank = cursor.fetchone()

    # rank 테이블에서 랭크 정보 가져오기
    cursor.execute('''
        SELECT rank, exp
        FROM rank
        ORDER BY exp
    ''')
    ranks = cursor.fetchall()

    # 승급 여부 확인
    for rank_info in ranks:
        rank_name, exp = rank_info

        if new_exp >= exp and current_exp < exp:
            # 새로운 랭크로 업데이트
            cursor.execute('''
                UPDATE human
                SET rank = %s
                WHERE human_id = %s
            ''', (rank_name, human_id))

            print(f"축하합니다! 티어가 {rank_name}로 상승하였습니다.")
            break  # 승급 조건을 만족하면 더 이상 확인하지 않고 종료


# 인벤토리 아이템 정보 보기
def view_inventory_items(human_id):
    cursor.execute('''
        SELECT i.item_id, i.item_name, i.item_type
        FROM inventory i
        WHERE i.human_id = %s
    ''', (human_id,))
    inventory_items = cursor.fetchall()

    if not inventory_items:
        print("인벤토리에 아이템이 없습니다.")
    else:
        print("--- 인벤토리 아이템 정보 ---")
        for item in inventory_items:
            print(f"아이템 ID: {item[0]}/아이템 이름: {item[1]}/아이템 타입: {item[2]}")
            print("-------------")


# 인벤토리 무기 정보 보기
def view_inventory_weapons(human_id):
    # inventory_weapons_view라는 view활용
    cursor.execute('''
        SELECT ivw.item_id, ivw.weapon_name, ivw.attack, ivw.durability
        FROM inventory_weapons_view ivw
        WHERE ivw.human_id = %s
    ''', (human_id,))
    inventory_weapons = cursor.fetchall()

    if not inventory_weapons:
        print("인벤토리에 무기가 없습니다.")
    else:
        print("--- 인벤토리 무기 정보 ---")
        for weapon in inventory_weapons:
            print(f"무기 ID: {weapon[0]}/무기 이름: {weapon[1]}/무기 공격력: {weapon[2]}/무기 내구도: {weapon[3]}")
            print("-------------")


# 물약 정보 보기
def view_inventory_potions(human_id):
    # inventory_potions_view라는 view활용
    cursor.execute('''
        SELECT item_id, potion_name, count, heal
        FROM inventory_potions_view
        WHERE human_id = %s
    ''', (human_id,))
    potions = cursor.fetchall()

    if not potions:
        print("인벤토리에 물약이 없습니다.")
    else:
        print("--- 물약 정보 ---")
        for potion in potions:
            print(f"물약 ID: {potion[0]}/물약 이름: {potion[1]}/물약 개수: {potion[2]}/물약 치유량: {potion[3]}")
            print("-------------")


# 무기 장착
def equip_weapon(human_id):
    cursor.execute('''
        SELECT i.item_id, w.attack
        FROM inventory i
        JOIN human_weapon w ON i.item_id = w.weapon_id
        WHERE i.human_id = %s AND i.item_type = 'weapon'
    ''', (human_id,))

    inventory_weapons = cursor.fetchall()

    # 사용자에게 무기 ID 입력 받기
    weapon_id = input("장착할 무기의 ID를 입력하세요: ")

    # 선택한 무기가 인벤토리에 있는지 확인
    if any(weapon_id == weapon[0] for weapon in inventory_weapons):
        # 선택한 무기를 장착
        cursor.execute('''
            UPDATE human
            SET equipped_weapon_id = %s, attack = %s
            WHERE human_id = %s
        ''', (weapon_id, get_weapon_attack(weapon_id), human_id))

        con.commit()
        print("무기를 장착했습니다.")
    else:
        print("잘못된 무기 ID입니다. 다시 확인해주세요.")


# 무기의 공격력을 가져오는 함수
def get_weapon_attack(weapon_id):
    cursor.execute('''
        SELECT attack
        FROM human_weapon
        WHERE weapon_id = %s
    ''', (weapon_id,))
    result = cursor.fetchone()
    return result[0] if result else 2


# 무기 해제
def unequip_weapon(human_id):
    # 현재 장착된 무기 확인
    cursor.execute('''
        SELECT equipped_weapon_id
        FROM human
        WHERE human_id = %s
    ''', (human_id,))
    equipped_weapon_id = cursor.fetchone()

    if not equipped_weapon_id:
        print("현재 장착된 무기가 없습니다.")
        return

    equipped_weapon_id = equipped_weapon_id[0]

    # 장착된 무기 정보 가져오기
    cursor.execute('''
        SELECT hw.weapon_name, hw.attack
        FROM human_weapon hw
        WHERE hw.weapon_id = %s
    ''', (equipped_weapon_id,))
    equipped_weapon_info = cursor.fetchone()
    if equipped_weapon_info:
        # 인간 정보에서 장착된 무기 해제
        cursor.execute('''
            UPDATE human
            SET equipped_weapon_id = NULL, attack = %s
            WHERE human_id = %s
        ''', (get_default_attack(), human_id))
        print(f"{equipped_weapon_info[0]} 무기 해제.")
    else:
        print("장착된 무기가 없습니다.")
    con.commit()


# 기본 공격력을 가져오는 함수
def get_default_attack():
    return 2


# 물약 섭취
def consume_potion(human_id):
    # 사용자에게 물약 ID 및 수량 입력 받기
    potion_id = input("섭취할 물약의 ID: ")
    quantity = int(input("섭취할 물약의 개수: "))

    # 물약이 인벤토리에 있는지 확인
    cursor.execute('''
           SELECT item_id, item_name, item_type
           FROM inventory
           WHERE human_id = %s AND item_id = %s AND item_type = 'potion'
       ''', (human_id, potion_id))
    potion = cursor.fetchone()

    if not potion or potion[2] != 'potion':
        print("인벤토리에 해당 물약이 없습니다.")
        return

    # 물약의 수량이 충분한지 확인
    cursor.execute('''
           SELECT count, heal
           FROM human_potion
           WHERE potion_id = %s
       ''', (potion_id,))
    potion_info = cursor.fetchone()
    count, heal = potion_info

    if not potion_info or quantity > count:
        print("물약의 수량이 부족합니다.")
        return

    # 현재 체력 계산
    cursor.execute('''
        SELECT h.hp
        FROM human h
        WHERE h.human_id = %s
    ''', (human_id,))
    current_hp = int(cursor.fetchone()[0])

    # 물약을 human_potion에서 찾아 count만큼 수량 감소
    cursor.execute('''
            UPDATE human_potion
            SET count = count - %s
            WHERE potion_id = %s
        ''', (quantity, potion_id))

    if count == quantity:
        # 물약을 인벤토리에서 제거
        cursor.execute('''
                   DELETE FROM inventory
                   WHERE human_id = %s AND item_id = %s
               ''', (human_id, potion_id))

    # 현재 체력 및 회복량을 이용하여 새로운 체력 계산
    new_hp = min(current_hp + heal * quantity, 100)

    # 인간의 체력 업데이트
    cursor.execute('''
           UPDATE human
           SET hp = %s
           WHERE human_id = %s
       ''', (new_hp, human_id))

    con.commit()
    print(f"{potion[1]} {quantity}개를 섭취하여 체력을 총 {heal * quantity} 회복했습니다. 현재 체력: {new_hp}")


# 상점 보기
def view_shop():
    cursor.execute('''
        SELECT * FROM item_shop
    ''')
    items = cursor.fetchall()

    if items:
        print("--- 상점 ---")
        print('{:<20}{:<15}'.format("item_name", "item_type"))
        print('{:<20}{:<15}'.format("-------------", "----------"))
        for item in items:
            print('{:<20}{:<15}'.format(item[0], item[1]))
        print("-------------")
    else:
        print("상점에 물건이 없습니다.")


# 고른 아이템의 정보 보기
def choose_item_info(item_name):
    # 아이템 타입에 따라 테이블을 선택하여 정보를 가져오기
    cursor.execute('''
        SELECT i.item_name, i.item_type, 
               CASE WHEN i.item_type = 'weapon' THEN w.attack
                    WHEN i.item_type = 'potion' THEN p.heal
                    ELSE NULL END AS additional_info,
               CASE WHEN i.item_type = 'weapon' THEN w.price
                    WHEN i.item_type = 'potion' THEN p.price
                    ELSE NULL END AS price,
               CASE WHEN i.item_type = 'weapon' THEN w.durability
                    ELSE NULL END AS durability
        FROM item_shop i
        LEFT JOIN weapon w ON i.item_name = w.weapon_name
        LEFT JOIN potion p ON i.item_name = p.potion_name
        WHERE i.item_name = %s
    ''', (item_name,))

    item_info = cursor.fetchone()

    if item_info:
        item_name, item_type, additional_info, price, durability = item_info
        print(f"아이템 이름: {item_name}")
        print(f"아이템 타입: {item_type}")
        if additional_info is not None:
            if item_type == 'potion':
                print(f"회복력: {additional_info}")
            else:
                print(f"공격력: {additional_info}")
        print(f"가격: {price}")
        if durability is not None:
            print(f"내구도: {durability}")
        return True
    else:
        print("해당 아이템이 존재하지 않습니다.")
        return False


# 아이템 구입
def purchase_item(human_id):
    # 사용자에게 구입할 아이템 이름 입력 받기
    item_name = input("구입할 아이템의 이름을 입력하세요: ")

    # 선택한 아이템의 정보 출력
    if not choose_item_info(item_name):
        return
    choice = str(input("구매하시겠습니까?\n"
                       "YES | NO\n"))

    if choice.lower() != "yes":
        print("구매 취소")
        return

    # 아이템의 총 가격 계산
    # 아이템 타입에 따라 테이블을 선택하여 가격 정보를 가져오기
    cursor.execute('''
           SELECT i.item_type,
                   CASE WHEN item_type = 'weapon' THEN w.price
                        WHEN item_type = 'potion' THEN p.price
                        ELSE NULL END AS price
           FROM item_shop i
           LEFT JOIN weapon w ON i.item_name = w.weapon_name
           LEFT JOIN potion p ON i.item_name = p.potion_name
           WHERE i.item_name = %s
       ''', (item_name,))

    result = cursor.fetchone()
    item_type, item_price = result

    # 사용자의 돈 확인
    cursor.execute('''
        SELECT money
        FROM human
        WHERE human_id = %s
    ''', (human_id,))
    user_money = cursor.fetchone()[0]

    if int(user_money) < int(item_price):
        print("돈이 부족하여 아이템을 구입할 수 없습니다.")
        return

    # 구입한 아이템을 인벤토리, human_weapon, human_potion에 추가
    # 무기인 경우
    if item_type == 'weapon':
        cursor.execute('''
            INSERT INTO human_weapon (weapon_id, weapon_name, attack, durability)
            SELECT
                COALESCE((SELECT MAX(CAST(weapon_id AS INTEGER)) + 1 FROM human_weapon), 1),
                weapon_name,
                attack,
                durability
            FROM weapon
            WHERE weapon_name = %s
        ''', (item_name,))

        cursor.execute('''
            INSERT INTO inventory (human_id, item_id, item_name, item_type)
            VALUES
                (%s, COALESCE((SELECT MAX(CAST(weapon_id AS INTEGER))  FROM human_weapon), 1), %s, %s)
        ''', (human_id, item_name, item_type))


    # 물약인 경우
    elif item_type == 'potion':
        # 이미 보유 중인 물약인지 확인
        cursor.execute('''
                SELECT count
                FROM human_potion hp
                JOIN inventory i ON hp.potion_name = i.item_name
                WHERE hp.potion_name = %s AND i.human_id = %s
            ''', (item_name, human_id))
        existing_count = cursor.fetchone()

        if existing_count:
            # 이미 보유 중인 물약이면 count만 증가
            cursor.execute('''
                UPDATE human_potion
                SET count = count + 1
                WHERE potion_id IN (SELECT hp.potion_id
                                    FROM human_potion hp
                                    JOIN inventory i ON hp.potion_id = i.item_id
                                    WHERE hp.potion_name = %s AND i.human_id = %s)
            ''', (item_name, human_id))
        else:
            # 보유 중이 아니면 새로 추가
            cursor.execute('''
                    INSERT INTO human_potion (potion_id, potion_name, count, heal)
                    VALUES (
                        COALESCE((SELECT MAX(CAST(potion_id AS INTEGER)) + 1 FROM human_potion), 1),
                        %s,
                        1,
                        (SELECT heal FROM potion WHERE potion_name = %s)
                    )
                ''', (item_name, item_name))

            # 구입한 아이템을 인벤토리, human_weapon, human_potion에 추가
            cursor.execute('''
                    INSERT INTO inventory (human_id, item_id, item_name, item_type)
                    VALUES (
                        %s,
                        COALESCE((SELECT MAX(CAST(potion_id AS INTEGER)) FROM human_potion), 1),
                        %s,
                        %s
                    )
                ''', (human_id, item_name, item_type))

    else:
        print("")
        return
    # 사용자의 돈 감소
    cursor.execute('''
        UPDATE human
        SET money = money - %s
        WHERE human_id = %s
    ''', (item_price, human_id))

    con.commit()
    print("아이템을 성공적으로 구입했습니다.")


if __name__ == "__main__":
    con = psycopg2.connect(
        database='project',
        user='db2023',
        password='db!2023',
        host='::1',
        port='5432'
    )
    cursor = con.cursor()
    mode = mode_set()
    if mode == 1:
        run_game()
    elif mode == 2:
        developer_mod()

    # 데이터베이스 연결 종료
    con.close()
