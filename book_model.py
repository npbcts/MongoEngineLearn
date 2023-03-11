from mongoengine import connect, disconnect
from mongoengine import Document
from mongoengine import StringField, IntField
from mongo_config import TEST_DB1, TEST_DB2, TEST_DB3, HOST, PORT, USERNAME, PASSWORD

from mongoengine import BooleanField, DateTimeField, DictField, EmailField, FloatField, ListField, ReferenceField
from mongoengine import EmbeddedDocument, EmbeddedDocumentField, LazyReferenceField

# 连接到已创建的数据库
connect(TEST_DB1, host=HOST, port=PORT, username=USERNAME, password=PASSWORD, authentication_source=TEST_DB1, alias=TEST_DB1)
connect(TEST_DB2, host=HOST, port=PORT, username=USERNAME, password=PASSWORD, authentication_source=TEST_DB2, alias=TEST_DB2)
connect(TEST_DB3, host=HOST, port=PORT, username=USERNAME, password=PASSWORD, authentication_source=TEST_DB3, alias=TEST_DB3)


class BookType(Document):
    type_name = StringField()
    meta = {"db_alias": TEST_DB1}

    
class BookAuthor(Document):
    author_name = StringField()
    meta = {"db_alias": TEST_DB1}


class Seller(Document):
    name = StringField()
    phone = StringField(regex="^\d+")
    meta = {"db_alias": TEST_DB1}


class PublishingHouse(EmbeddedDocument):
    name =  StringField()  # unique=True,注意范围
    address =  StringField()
    phone =  StringField()  
    # 两次生成的字段不一致, 第二次生成包含 address；第一次生成 phone。本模型添加两个字段后，就可以正常运行。

    
class BookAllField(Document):
    bookid = StringField(unique=True)
    name = StringField()
    ifnewbook = BooleanField()  # 是否为新上架图书
    shelves_date = DateTimeField()
    author = ReferenceField(BookAuthor)  # 使引用字段执行其他集合
    author_email = EmailField()
    price = FloatField()
    book_type = ReferenceField(BookType, dbref=True)  # 将引用ref文档
    publishing_house = EmbeddedDocumentField(PublishingHouse)
    seller = LazyReferenceField(Seller, dbref=True)
    tag = ListField()
    meta = {
        "db_alias": TEST_DB1,
         "indexes": [  # 数据集合创建时，并没有添加索引；没有在模型中和数据库中手动添加。
            "bookid",  # 此处的索引添加后，运行查询不久,已生效在数据库中添加索引，即数据库本身并和此处保持一致。
            #"name",  #从此处删除索引后，数据库中并没有删除对应的索引项目
            "price",
            "book_type",
            "publishing_house",
            "seller",
            "shelves_date"
        ]
    }
