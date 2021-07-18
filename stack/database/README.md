Даны таблицы

---------------------------------------------------------------------------------------------------
if object_id('stack.OrderItems') is not null
   drop table stack.OrderItems;
go

if object_id('stack.Orders') is not null
   drop table stack.Orders;
go

if object_id('stack.Customers') is not null
   drop table stack.Customers;
go


-- Заказчики
create table stack.Customers
(
   row_id int identity not null,
   name nvarchar(max) not null,           -- наименование заказчика

   constraint PK_Customers
      primary key nonclustered(row_id)
);
go

-- Заказы
create table stack.Orders
(
   row_id int identity not null,
   parent_id int,                         -- row_id родительской группы
   group_name nvarchar(max),              -- наименование группы заказов
   customer_id int,                       -- row_id заказчика
   registered_at date                     -- дата регистрации заказа

   constraint PK_Orders
      primary key nonclustered (row_id),
   constraint FK_Orders_Folder 
      foreign key (parent_id) 
      references stack.Orders(row_id)
      on delete no action
      on update no action,
   constraint FK_Customers
      foreign key (customer_id)
      references stack.Customers(row_id)
      on delete cascade
      on update cascade
);
go

-- Позиции заказов
create table stack.OrderItems
(
   row_id int identity not null,
   order_id int not null,                 -- row_id заказа
   name nvarchar(max) not null,           -- наименование позиции
   price int not null,                    -- стоимость позиции в рублях

   constraint PK_OrderItems
      primary key nonclustered (row_id),
   constraint FK_OrderItems_Orders
      foreign key (order_id) 
      references stack.Orders(row_id)
      on delete cascade
      on update cascade
);
go
---------------------------------------------------------------------------------------------------

Таблица Customers содержит информацию о покупателях интернет-магазина, таблица Orders - сведения о 
заказах, а таблица OrderItems - позиции в заказах. Данные в таблице Orders имеют древовидную структуру. 
Записи, у которых поле group_name не равно null, предназначены для группировки заказов по категориям. 
Такие записи не связаны с заказчиком, не имеют даты регистрации и связанных позиций в таблице OrderItems,
но могут содержать в себе заказы или другие группы. Если же поле group_name равно null, то запись является
заказом. Она обязательно связана с покупателем, имеет позиции и дату регистрации, но не может иметь 
вложенных заказов. Записи связываются с родительской группой с помощью поля parent_id, которое хранит
row_id этой группы. Записи с parent_id равным null считаются корневыми. Заказ может иметь несколько позиций
с одинаковым наименованием.

В таблицах имеются следующие данные:

---------------------------------------------------------------------------------------------------
insert into stack.Customers                                                               -- 1
values(N'Иванов');
insert into stack.Customers                                                               -- 2
values(N'Петров');
insert into stack.Customers                                                               -- 3
values(N'Сидоров');
insert into stack.Customers                                                               -- 4
values(N'ИП Федоров');


insert into stack.Orders(parent_id, group_name, customer_id, registered_at)               -- 1
values (null, N'Все заказы', null, null);

   insert into stack.Orders(parent_id, group_name, customer_id, registered_at)            -- 2
   values (1, N'Частные лица', null, null);

      insert into stack.Orders(parent_id, group_name, customer_id, registered_at)         -- 3
      values (2, N'Оргтехника', null, null);

         insert into stack.Orders(parent_id, group_name, customer_id, registered_at)      -- 4
         values (3, null, 1, '2019/10/02');

         insert into stack.Orders(parent_id, group_name, customer_id, registered_at)      -- 5
         values (3, null, 1, '2020/05/17');

       insert into stack.Orders(parent_id, group_name, customer_id, registered_at)        -- 6
         values (3, null, 1, '2020/04/28');

       insert into stack.Orders(parent_id, group_name, customer_id, registered_at)        -- 7
         values (3, null, 2, '2019/08/05');

       insert into stack.Orders(parent_id, group_name, customer_id, registered_at)        -- 8
         values (3, null, 2, '2020/05/17');

       insert into stack.Orders(parent_id, group_name, customer_id, registered_at)        -- 9
         values (3, null, 2, '2020/02/11');

      insert into stack.Orders(parent_id, group_name, customer_id, registered_at)         -- 10
      values (2, N'Канцелярия', null, null);

         insert into stack.Orders(parent_id, group_name, customer_id, registered_at)      -- 11
         values (10, null, 3, '2020/04/09');

   insert into stack.Orders(parent_id, group_name, customer_id, registered_at)            -- 12
   values (1, N'Юридические лица', null, null);

      insert into stack.Orders(parent_id, group_name, customer_id, registered_at)         -- 13
      values (12, null, 4, '2020/06/25');


insert into stack.OrderItems(order_id, name, price)
values (4, N'Принтер', 30);
insert into stack.OrderItems(order_id, name, price)
values (4, N'Факс', 20);


insert into stack.OrderItems(order_id, name, price)
values (5, N'Принтер', 50);
insert into stack.OrderItems(order_id, name, price)
values (5, N'Кассовый аппарат', 40);
insert into stack.OrderItems(order_id, name, price)
values (5, N'Факс', 30);


insert into stack.OrderItems(order_id, name, price)
values (6, N'Кассовый аппарат', 30);
insert into stack.OrderItems(order_id, name, price)
values (6, N'Кассовый аппарат', 40);


insert into stack.OrderItems(order_id, name, price)
values (7, N'Копировальный аппарат', 50);
insert into stack.OrderItems(order_id, name, price)
values (7, N'Калькулятор', 10);
insert into stack.OrderItems(order_id, name, price)
values (7, N'Кассовый аппарат', 60);


insert into stack.OrderItems(order_id, name, price)
values (8, N'Принтер', 50);
insert into stack.OrderItems(order_id, name, price)
values (8, N'Калькулятор', 10);


insert into stack.OrderItems(order_id, name, price)
values (9, N'Телефонный аппарат', 50);
insert into stack.OrderItems(order_id, name, price)
values (9, N'Кассовый аппарат', 40);


insert into stack.OrderItems(order_id, name, price)
values (11, N'Бумага', 2);
insert into stack.OrderItems(order_id, name, price)
values (11, N'Ручки', 1);


insert into stack.OrderItems(order_id, name, price)
values (13, N'Кулер', 100);
insert into stack.OrderItems(order_id, name, price)
values (13, N'Стулья', 70);
insert into stack.OrderItems(order_id, name, price)
values (13, N'Факс', 20);
go
---------------------------------------------------------------------------------------------------

Корневой группой является запись "Все заказы", в нее вложены группы "Частные лица" и "Юридические лица".
Примером заказа является запись "ИП Федоров", которая находится в группе "Юридические лица".


== Задание 1.

Написать функцию select_orders_by_item_name. Она получает один аргумент - наименование позиции (строка),
и должна найти все заказы, в которых имеется позиция с данным наименованием. Кроме того, она должна
подсчитать количество позиций с указанным наименованием в каждом отдельном заказе. Результатом вызова
функции должна быть таблица с тремя колонками:

- order_id (row_id заказа)
- customer (наименование заказчика)
- items_count (количество позиций с данным наименованием в этом заказе)

Примеры вызова функции:

select * from stack.select_orders_by_item_name(N'Факс')
-- 4     Иванов         1
-- 5     Иванов         1
-- 13    ИП Федоров     1

select * from stack.select_orders_by_item_name(N'Кассовый аппарат')
-- 5     Иванов         1
-- 6     Иванов         2
-- 7     Петров         1
-- 9     Петров         1

select * from stack.select_orders_by_item_name(N'Стулья')
-- 13    ИП Федоров     1


== Задание 2.

Написать функцию calculate_total_price_for_orders_group. Она получает row_id группы (либо заказа),
и возвращает суммарную стоимость всех позиций всех заказов в этой группе (заказе), причем 
суммирование должно выполняться по всему поддереву заказов, начинающемуся с данной группы.
Функция должна возвращать число.

Примеры вызова функции:

select stack.calculate_total_price_for_orders_group(1) as total_price   -- 703, все заказы
select stack.calculate_total_price_for_orders_group(2) as total_price   -- 513, группа 'Частные лица'
select stack.calculate_total_price_for_orders_group(3) as total_price   -- 510, группа 'Оргтехника'
select stack.calculate_total_price_for_orders_group(12) as total_price  -- 190, группа 'Юридические лица'
select stack.calculate_total_price_for_orders_group(13) as total_price  -- 190, заказ 'ИП Федоров'


== Задание 3.

Написать запрос, возвращающий наименования всех покупателей, у которых каждый заказ в 2020 году содержит
как минимум одну позициию с наименованием "Кассовый аппарат".

Результатом выполнения запроса на тестовых данных будет таблица с одной строкой "Иванов".