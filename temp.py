def deco(MyClass: type) -> type:
    class NewClass:
        pass

    for key, val in MyClass.__dict__.items():
        setattr(NewClass, f"_{key}", val)
    return NewClass


@deco
class Hoge:
    x: int


hoge = Hoge()
hoge.x
