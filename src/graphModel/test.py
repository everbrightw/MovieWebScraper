from src.graphModel.actor import Actor
from src.graphModel.film import Film

if __name__ == '__main__':
    test = Actor(name='wys', age=18, nationality='china', total_gross=0)
    print(test.name)

    test_film = Film(name='film', actors=['wys', 'wys2'], year=1998, total_gross=199998)
    print(test_film.actors)