create table if not exists customers
(
    id         serial
        primary key,
    name       varchar(100) not null,
    email      varchar(100) not null
        unique,
    created_at timestamp default now()
);

create table if not exists orders
(
    id           serial
        primary key,
    customer_id  integer        not null
        references customers,
    order_date   timestamp default now()
);

create table if not exists suppliers
(
    id            serial
        primary key,
    name          varchar(100) not null,
    contact_name  varchar(100),
    contact_email varchar(100),
    phone         varchar(20),
    address       varchar(200),
    city          varchar(100),
    country       varchar(100),
    created_at    timestamp default now()
);

create table if not exists categories
(
    id          serial
        primary key,
    name        varchar(100) not null
        unique,
    description text,
    created_at  timestamp default now()
);

create table if not exists products
(
    id             serial
        primary key,
    name           varchar(100)   not null,
    description    text,
    price          numeric(10, 2) not null,
    stock_quantity integer        not null,
    created_at     timestamp default now(),
    category_id    integer
        references categories,
    supplier_id    integer
        references suppliers
);

create table if not exists order_items
(
    id         serial
        primary key,
    order_id   integer        not null
        references orders,
    product_id integer        not null
        references products,
    quantity   integer        not null,
    price      numeric(10, 2) not null
);

create table if not exists reviews
(
    id          serial
        primary key,
    product_id  integer not null
        references products,
    customer_id integer not null
        references customers,
    rating      integer
        constraint reviews_rating_check
            check ((rating >= 1) AND (rating <= 5)),
    comment     text,
    review_date timestamp default now()
);

create table if not exists payments
(
    id             serial
        primary key,
    order_id       integer        not null
        references orders,
    payment_date   timestamp default now(),
    amount         numeric(10, 2) not null,
    payment_method varchar(50)
);

create table if not exists shippings
(
    id              serial
        primary key,
    order_id        integer not null
        references orders,
    shipping_date   timestamp,
    shipping_method varchar(50),
    tracking_number varchar(100),
    status          varchar(50)
);

create table if not exists wishlists
(
    id          serial
        primary key,
    customer_id integer not null
        references customers,
    created_at  timestamp default now()
);

create table if not exists wishlist_items
(
    id          serial
        primary key,
    wishlist_id integer not null
        references wishlists,
    product_id  integer not null
        references products,
    added_at    timestamp default now()
);

create table if not exists carts
(
    id          serial
        primary key,
    customer_id integer not null
        references customers,
    created_at  timestamp default now()
);

create table if not exists cart_items
(
    id         serial
        primary key,
    cart_id    integer not null
        references carts,
    product_id integer not null
        references products,
    quantity   integer not null,
    added_at   timestamp default now()
);

create table if not exists returns
(
    id            serial
        primary key,
    order_item_id integer not null
        references order_items,
    return_date   timestamp default now(),
    reason        varchar(200),
    status        varchar(50)
);

create table if not exists promotions
(
    id                  serial
        primary key,
    name                varchar(100) not null,
    description         text,
    discount_percentage numeric(5, 2)
        constraint promotions_discount_percentage_check
            check ((discount_percentage > (0)::numeric) AND (discount_percentage <= (100)::numeric)),
    start_date          timestamp    not null,
    end_date            timestamp    not null
);

create table if not exists product_promotions
(
    id           serial
        primary key,
    product_id   integer not null
        references products,
    promotion_id integer not null
        references promotions
);

