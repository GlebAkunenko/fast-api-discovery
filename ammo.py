def bullet(user: int, event: int, state: bool) -> str:
    data = '{' + f'"user":{user},"event":{event},"subscribe":{str(state).lower()}' + '}\n'
    header = f"{len(data)-1} /add\n"
    return header + data


from random import randint, random

def make_file(n: int, user_range: tuple[int, int], event_range: tuple[int, int]):
    with open('ammo.txt', 'a') as file:
        for i in range(n):
            file.write(bullet(
                user=(user_range[0] + i) % user_range[1],
                event=(event_range[0] + i) % event_range[1],
                state=(random() < 0.5)
            ))


if __name__ == "__main__":
    make_file(50_000, (1, 5000), (1, 500_000))
