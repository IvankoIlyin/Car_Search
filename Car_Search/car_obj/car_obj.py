
class car_obj:
    def __init__(self,title=None,price=None,information=None,description=None,link=None):
        self.title=title
        self.price=price
        self.information=information
        self.description=description
        self.link=link


class Search_List:
    def __init__(self, title=None, price=None, info=None,descr=None):
        self.title=title
        self.price=price
        self.info=info
        self.desc = descr


class Car:
    def __init__(self,mark=None,model=None,price:[]=None,year:[]=None,characteristic=None,dedescription=None):
        self.mark=mark
        self.model=model
        self.price=price
        self.year=year
        self.characteristics=characteristic
        self.dedescription=dedescription

class Characteristic:
    def __init__(self, keys: list[str], value: list[str] = None):
        self.keys = keys
        self.value = value if value is not None else []

class Car_Characteristics:
    def __init__(self,salesman=None,transmission=None,fuel_type=None,engine_capacity=None,drive_type=None,
                 body_type=None,color=None,seats=None,mileage=None,fuel_costs=None,location=None):

        self.salesman = Characteristic(["Продавець", "Оголошення від"],salesman)
        self.transmission = Characteristic(["Коробка передач", "Коробка"],transmission)
        self.fuel_type = Characteristic(["Тип палива", "Паливо"],fuel_type)
        self.engine_capacity = Characteristic(["Двигун"],engine_capacity)
        self.drive_type = Characteristic(["Привід"],drive_type)
        self.body_type = Characteristic(["Тип кузова"],body_type)
        self.color = Characteristic(["Колір"],color)
        self.seats = Characteristic(["Місць в салоні","Кількість дверей"],seats)
        self.mileage = Characteristic(["Пробіг"],mileage)
        self.fuel_costs = Characteristic(["Витрати пального"],fuel_costs)
        self.location = Characteristic(["Місто"],location)
        self.all_info=[self.salesman,self.transmission,self.fuel_type,self.engine_capacity,self.drive_type,
                       self.body_type,self.color,self.seats,self.mileage,self.fuel_costs,self.location]



    def check_value_in_list(self,value_keys,s1):
        for i in value_keys:
            if s1.find(i)!=-1:
                return True

    def add_attr(self, s1: str, s2: str):
        for attr, value in self.__dict__.items():
            if isinstance(value, Characteristic):
                if s1 in value.keys or self.check_value_in_list(value.keys,s1)==True and s2!='':
                    value.value.append(s2)




    def display_all_characteristics(self):
        for attr, value in self.__dict__.items():
            if isinstance(value, Characteristic):
                print(f"{attr}: {value.value}")





# car_char=Car_Characteristics()
#
#
# car_char.add_attr("Витрати пального (л/100 км)","місто 7.7• траса 5.7• змішаний 6.4")
#
# car_char.display_all_characteristics()