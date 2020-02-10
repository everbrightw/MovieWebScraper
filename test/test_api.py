import logging
from unittest import TestCase

from src import app
import json

from src.analysis import plot_gross_dict, find_movies_years_total_gross, find_age_group_total_gross_avg, find_hub_actor, \
    find_age_group_total_gross
from src.graphModel.graph import Graph, from_json_to_graph

with open('/Users/yusenwang/cs242/hw2/fa19-cs242-assignment2/src/graphModel/data.json',
          encoding='utf-8') as json_file:
    data = json.load(json_file)

    data_actor = data[0]  # actor index
    data_movie = data[1]  # movie index


class ApiTest(TestCase):
    def setUp(self):
        self.app = app.app.test_client()

    def test_get_actor(self):
        """
        test get actor
        :return:
        """
        response = self.app.get('actors/not-found-test')
        response = self.app.get('actors/Reginald_VelJohnson')
        assert (response.json == {"Reginald VelJohnson": {
            "json_class": "Actor",
            "name": "Reginald VelJohnson",
            "age": 64,
            "total_gross": 380,
            "movies": [
                "Wolfen",
                "Ghostbusters",
                "Remo Williams: The Adventure Begins",
                "Crocodile Dundee",
                "Plain Clothes",
                "Die Hard",
                "Turner & Hooch",
                "Die Hard 2",
                "Posse",
                "Ground Zero",
                "Like Mike",
                "Death to the Supermodels",
                "Three Days to Vegas",
                "Steppin: The Movie",
                "You Again",
                "Air Collision"
            ]
        }
        })

    def test_get_actor_by_attr(self):
        """
        test get actor by attribute
        :return:
        """
        response = self.app.get('actors?name=Bruce_Willis')
        assert (response.json == {"Bruce Willis": {
            "json_class": "Actor",
            "name": "Bruce Willis",
            "age": 61,
            "total_gross": 562709189,
            "movies": [
                "The First Deadly Sin",
                "The Verdict",
                "Blind Date",
                "Sunset",
                "Die Hard",
                "In Country",
                "Look Who's Talking",
                "That's Adequate",
                "Die Hard 2",
                "Look Who's Talking Too",
                "The Bonfire of the Vanities",
                "Mortal Thoughts",
                "Hudson Hawk",
                "Billy Bathgate",
                "The Last Boy Scout",
                "The Player",
                "Death Becomes Her",
                "Loaded Weapon 1",
                "Striking Distance",
                "Color of Night",
                "North",
                "Pulp Fiction",
                "Nobody's Fool",
                "Die Hard with a Vengeance",
                "Four Rooms",
                "12 Monkeys",
                "Last Man Standing",
                "Beavis and Butt-Head Do America",
                "The Fifth Element",
                "The Jackal",
                "Mercury Rising",
                "Armageddon",
                "The Siege",
                "Breakfast of Champions",
                "The Sixth Sense",
                "The Story of Us",
                "The Whole Nine Yards",
                "Disney's The Kid",
                "Unbreakable",
                "Bandits",
                "Hart's War",
                "True West",
                "The Crocodile Hunter: Collision Course",
                "Grand Champion",
                "Tears of the Sun",
                "Rugrats Go Wild",
                "Charlie's Angels: Full Throttle",
                "The Whole Ten Yards",
                "Ocean's Twelve",
                "Hostage",
                "Sin City",
                "Alpha Dog",
                "16 Blocks",
                "Fast Food Nation",
                "Lucky Number Slevin",
                "Over the Hedge",
                "Hammy's Boomerang Adventure",
                "The Astronaut Farmer",
                "Perfect Stranger",
                "Grindhouse",
                "Planet Terror",
                "Nancy Drew",
                "Live Free or Die Hard",
                "What Just Happened",
                "Assassination of a High School President",
                "Surrogates",
                "Cop Out",
                "The Expendables",
                "Red",
                "Set Up",
                "Catch .44",
                "Moonrise Kingdom",
                "Lay the Favorite",
                "The Expendables 2",
                "The Cold Light of Day",
                "Looper",
                "Fire with Fire",
                "A Good Day to Die Hard",
                "G.I. Joe: Retaliation",
                "Red 2",
                "Sin City: A Dame to Kill For",
                "The Prince",
                "Vice",
                "Rock the Kasbah",
                "Extraction",
                "Precious Cargo",
                "Marauders",
                "Split",
                "The Bombing",
                "Once Upon a Time in Venice",
                "First Kill",
                "Death Wish"
            ]
        }
        })

    def test_get_actor_by_attr1(self):
        """
        test get actor by attribute age
        :return:
        """
        response = self.app.get('actors?age=20')
        assert (response.json == {"Anya Taylor-Joy": {
            "age": 20,
            "json_class": "Actor",
            "movies": [
                "Vampire Academy",
                "The Witch:\nA New-England Folktale",
                "Morgan",
                "Barry",
                "Split",
                "Thoroughbred"
            ],
            "name": "Anya Taylor-Joy",
            "total_gross": 193
        }})

    def test_get_actor_by_attr2(self):
        """
        test actor by total_gross
        :return:
        """
        response = self.app.get('actors?total_gross=193')
        assert (response.json == {"Anya Taylor-Joy": {
            "age": 20,
            "json_class": "Actor",
            "movies": [
                "Vampire Academy",
                "The Witch:\nA New-England Folktale",
                "Morgan",
                "Barry",
                "Split",
                "Thoroughbred"
            ],
            "name": "Anya Taylor-Joy",
            "total_gross": 193
        },
            "Betty Buckley": {
                "age": 69,
                "json_class": "Actor",
                "movies": [
                    "Carrie",
                    "Tender Mercies",
                    "Wild Thing",
                    "Frantic",
                    "Another Woman",
                    "Rain Without Thunder",
                    "Wyatt Earp",
                    "Simply Irresistible",
                    "The Happening",
                    "Split"
                ],
                "name": "Betty Buckley",
                "total_gross": 193
            },
            "James McAvoy": {
                "age": 37,
                "json_class": "Actor",
                "movies": [
                    "Regeneration",
                    "Swimming Pool",
                    "Bright Young Things",
                    "Bollywood Queen",
                    "Wimbledon",
                    "Strings",
                    "Inside I'm Dancing",
                    "The Chronicles of Narnia: The Lion, the Witch and the Wardrobe",
                    "The Last King of Scotland",
                    "Starter for 10",
                    "Becoming Jane",
                    "Penelope",
                    "Atonement",
                    "Wanted",
                    "The Last Station",
                    "Gnomeo and Juliet",
                    "The Conspirator",
                    "X-Men: First Class",
                    "Arthur Christmas",
                    "Welcome to the Punch",
                    "Trance",
                    "Filth",
                    "Muppets Most Wanted",
                    "X-Men: Days of Future Past",
                    "The Disappearance of Eleanor Rigby",
                    "Victor Frankenstein",
                    "X-Men: Apocalypse",
                    "Split",
                    "The Coldest City",
                    "Submergence"
                ],
                "name": "James McAvoy",
                "total_gross": 193
            }})

    def test_get_movie_by_attr(self):
        response = self.app.get('movies?name=The_First_Deadly_Sin')

        assert (response.json == {"The First Deadly Sin": {
            "json_class": "Movie",
            "name": "The First Deadly Sin",
            "wiki_page": "https://en.wikipedia.org/wiki/The_First_Deadly_Sin",
            "box_office": 0,
            "year": 1980,
            "actors": [
                "Faye Dunaway",
                "James Whitmore",
                "David Dukes",
                "Brenda Vaccaro",
                "Martin Gabel",
                "Anthony Zerbe"
            ]
        }})

    def test_get_movie_by_attr1(self):
        response = self.app.get('movies?box_office=4594452')

        assert (response.json == {"Sunset": {
            "json_class": "Movie",
            "name": "Sunset",
            "wiki_page": "https://en.wikipedia.org/wiki/Sunset_(film)",
            "box_office": 4594452,
            "year": 1988,
            "actors": [
                "Bruce Willis",
                "James Garner",
                "Mariel Hemingway",
                "Kathleen Quinlan",
                "Jennifer Edwards",
                "Malcolm McDowell"
            ]
        }})

    def test_get_movie_by_attr3(self):
        """
        test get movie by attribute year
        :return:
        """
        response = self.app.get('movies?year=1998')

        assert (response.json == {"Armageddon": {
            "actors": [
                "Bruce Willis",
                "Billy Bob Thornton",
                "Liv Tyler",
                "Ben Affleck",
                "Will Patton",
                "Peter Stormare",
                "Keith David",
                "Steve Buscemi"
            ],
            "box_office": 553,
            "json_class": "Movie",
            "name": "Armageddon",
            "wiki_page": "https://en.wikipedia.org/wiki/Armageddon_(1998_film)",
            "year": 1998
        },
            "Chairman of the Board": {
                "actors": [
                    "Carrot Top",
                    "Courtney Thorne-Smith",
                    "Larry Miller (entertainer)",
                    "Raquel Welch",
                    "Mystro Clark",
                    "M. Emmet Walsh",
                    "Jack Warden"
                ],
                "box_office": 181233,
                "json_class": "Movie",
                "name": "Chairman of the Board",
                "wiki_page": "https://en.wikipedia.org/wiki/Chairman_of_the_Board_(film)",
                "year": 1998
            },
            "Mercury Rising": {
                "actors": [
                    "Bruce Willis",
                    "Alec Baldwin",
                    "Chi McBride",
                    "Kim Dickens"
                ],
                "box_office": 93,
                "json_class": "Movie",
                "name": "Mercury Rising",
                "wiki_page": "https://en.wikipedia.org/wiki/Mercury_Rising",
                "year": 1998
            },
            "The Siege": {
                "actors": [
                    "Denzel Washington",
                    "Annette Bening",
                    "Bruce Willis",
                    "Tony Shalhoub",
                    "Sami Bouajila",
                    "David Proval"
                ],
                "box_office": 116,
                "json_class": "Movie",
                "name": "The Siege",
                "wiki_page": "https://en.wikipedia.org/wiki/The_Siege_(1998_film)",
                "year": 1998
            },
            "Twilight": {
                "actors": [
                    "Paul Newman",
                    "Susan Sarandon",
                    "Gene Hackman",
                    "Stockard Channing",
                    "Reese Witherspoon",
                    "Giancarlo Esposito"
                ],
                "box_office": 15055091,
                "json_class": "Movie",
                "name": "Twilight",
                "wiki_page": "https://en.wikipedia.org/wiki/Twilight_(1998_film)",
                "year": 1998
            }})

    def test_get_movie_by_attr4(self):
        response = self.app.get('movies?actors=[Tom_Hanks]')

    def test_get_movie(self):
        """
        test get movie
        :return:
        """
        response = self.app.get('movies/not_found_movies')
        response = self.app.get('movies/Lucky_Number_Slevin')
        assert (response.json == {"Lucky Number Slevin": {
            "json_class": "Movie",
            "name": "Lucky Number Slevin",
            "wiki_page": "https://en.wikipedia.org/wiki/Lucky_Number_Slevin",
            "box_office": 56,
            "year": 0,
            "actors": [
                "Josh Hartnett",
                "Lucy Liu",
                "Bruce Willis",
                "Morgan Freeman",
                "Ben Kingsley",
                "Stanley Tucci"
            ]
        }})

    def test_post_actor(self):
        """
        test post actor
        :return:
        """
        response = self.app.post('/post_actors',
                                 data=json.dumps({"name": "Yusen Wang"}),
                                 content_type='application/json')
        assert "Yusen Wang" in response.json

    def test_post_movie(self):
        """
        test post movie
        :return:
        """
        response = self.app.post('/post_movies',
                                 data=json.dumps({"name": "Yusen Wang"}),
                                 content_type='application/json')
        assert "Yusen Wang" in response.json

    def test_put_movie(self):
        response = self.app.put('/movies/The_Pursuit_Of_Happiness',
                                data=json.dumps({"name": "The Pursuit Of Happiness"}),
                                content_type='application/json')
        assert "The Pursuit Of Happiness" in response.json

    def test_put_existing_movie(self):
        response = self.app.put('/movies/The_Verdict',
                                data=json.dumps({"name": "Name Changed"}),
                                content_type='application/json')

        assert "Name Changed" in response.json.get('The Verdict').get('name')

    def test_put_actor(self):
        response = self.app.put('/actors/Yusen_Wang',
                                data=json.dumps({"name": "Yusen Wang"}),
                                content_type='application/json')

        assert "Yusen Wang" in response.json

    def test_put_none_exist_actor(self):
        response = self.app.put('/actors/peter',
                                data=json.dumps({"name": "Yusen Wang"}),
                                content_type='application/json')
        assert "Yusen Wang" in response.json

    def test_delete_movie(self):
        """
        test delete movie
        :return:
        """
        response = self.app.delete('movies/Over_the_Hedge',
                                   content_type='application/json')
        assert "Over the Hedge" not in response.json

    def test_delete_actor(self):
        """
        test delete actor
        :return:
        """
        response = self.app.options('/print_info')
        response = self.app.delete('actors/David_Dukes',
                                   content_type='application/json')
        assert "David Dukes" not in response.json

    @staticmethod
    def test_data_analysis():
        """
        Test Data analysis by a reduced json file
        # test mainly depends on using an text editor to find the
        # number of appearance of an actor name to make sure the answer
        :return:
        """
        json_file_str = '/Users/yusenwang/cs242/hw2/fa19-cs242-assignment2/test/smaller_test_data.json'
        g = Graph()
        g = from_json_to_graph(json_file_str, g)
        g.print_graph()
        print(find_movies_years_total_gross(g))
        print(find_age_group_total_gross_avg(g))
        print(find_age_group_total_gross(g))
        plot_gross_dict(find_age_group_total_gross_avg(g))

        assert find_hub_actor(g) == 'Bruce Willis'
