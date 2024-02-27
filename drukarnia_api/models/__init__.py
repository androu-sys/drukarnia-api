from drukarnia_api.models.tools import *
from drukarnia_api.models.article import ArticleModel
from drukarnia_api.models.author import AuthorModel
from drukarnia_api.models.bookmark import BookmarkModel
from drukarnia_api.models.comment import CommentModel
from drukarnia_api.models.notification import NotificationModel, NotificationType
from drukarnia_api.models.relationship import AuthorRelationshipsModel
from drukarnia_api.models.socials import SocialsModel
from drukarnia_api.models.tag import TagModel


__all__ = [
    "BaseModel",
    "ModelField",
    "ModelRegistry",
    "ArticleModel",
    "AuthorModel",
    "BookmarkModel",
    "CommentModel",
    "NotificationType",
    "NotificationModel",
    "AuthorRelationshipsModel",
    "SocialsModel",
    "TagModel",
]


if __name__ == "__main__":
    data = {
    "id_": "65aac36c2e16847e21eb63c9",
    "title": "Пісня дібров — Павло Дерев'янко",
    "seoTitle": "Пісня дібров — Павло Дерев'янко",
    "description": "Вовча стежка, що вела героїв понад 10 років, добігла кінця. Дуже важко прощатися з направду чудовим, нашим фентезі made in Ukraine. “Пісня дібров” стала розгадкою, ключем до всіх недосказаних, незрозумілих, навмисно прихованих моментів історії характерників.",
    "picture": "https://cdn.drukarnia.com.ua/64807c9afb6c8702221188ed/images/articles/preview/GEFxk_Vxnl_Xb2UoMo8.jpeg",
    "thumbPicture": "https://cdn.drukarnia.com.ua/64807c9afb6c8702221188ed/images/articles/preview/GEFxk_Vxnl_Xb2UoMo8.webp",
    "mainTag": "Рецензії",
    "tags": [
        {
            "id_": "63d714e84b15077ac00bb245",
            "name": "Фентезі",
            "slug": "fentezi",
            "v__": 0,
            "createdAt": "2023-04-14T18:44:34.733Z",
            "default": False,
            "mentionsNum": 178
        },
        {
            "id_": "64204eacb4306ff6ba8c6c5b",
            "name": "Рецензії",
            "slug": "recenziyi",
            "v__": 0,
            "createdAt": "2023-04-14T18:44:34.733Z",
            "default": False,
            "mentionsNum": 111
        },
        {
            "id_": "643d5b96665d056f2cc76c9a",
            "name": "Українська Література",
            "slug": "ukrayinska-literatura",
            "v__": 0,
            "createdAt": "2023-04-17T14:45:42.500Z",
            "default": False,
            "mentionsNum": 99
        },
        {
            "id_": "656ddde57d851addfd63dbae",
            "name": "Павло Дерев'янко",
            "slug": "pavlo-derev-yanko",
            "v__": 0,
            "createdAt": "2023-12-04T14:10:45.363Z",
            "default": False,
            "ignore": False,
            "mentionsNum": 3
        },
        {
            "id_": "65aac36c8dbad5bea32e4c56",
            "name": "Пісня Дібров",
            "slug": "pisnya-dibrov",
            "v__": 0,
            "createdAt": "2024-01-19T18:46:04.415Z",
            "default": False,
            "ignore": False,
            "mentionsNum": 1
        }
    ],
    "ads": False,
    "index": False,
    "sensitive": False,
    "canonical": None,
    "likeNum": 1,
    "commentNum": 0,
    "readTime": 141,
    "slug": "pisnya-dibrov-pavlo-derev-yanko-cxKd2",
    "mainTagSlug": "recenziyi",
    "mainTagId": "64204eacb4306ff6ba8c6c5b",
    "createdAt": "2024-01-19T18:46:05.443Z",
    "authorArticles": [
        {
            "id_": "65c4b55a2e16847e21264779",
            "title": "Останнє королівство — Бернард Корнвелл",
            "description": "На початку в мене з книгою склалися непрості стосунки. Я не могла призвичаїтися до стилю автора, його виклад видавався мені кострубатим, події неслися “галопом по Європах”, а роки минали сторінка за сторінкою. Враження таке, наче читаєш не художню книгу, а літопис.",
            "owner": "64807c9afb6c8702221188ed",
            "picture": "https://cdn.drukarnia.com.ua/64807c9afb6c8702221188ed/images/articles/preview/IrRaE4p-ysk7FjaH4kS.jpeg",
            "mainTag": "Рецензії",
            "readTime": 108,
            "slug": "ostannye-korolivstvo-bernard-kornvell-7at6g",
            "mainTagSlug": "recenziyi",
            "mainTagId": "64204eacb4306ff6ba8c6c5b",
            "createdAt": "2024-02-08T11:04:59.657Z",
            "isBookmarked": False
        },
        {
            "id_": "658fc224c1d4e0d80e9c8875",
            "title": "Тенета війни — Павло Дерев’янко",
            "description": "“Тенета війни” — назва другої частини “Літопису Сірого Ордену” Павла Дерев’янка. Сім років минуло відтоді, як Северин, Ярема, Пилип і Гнат вступили до лав характерників. Героям всього по 23 роки, але їхні тіла пошрамовані, а душі обпалені війною зі Швецією.",
            "owner": "64807c9afb6c8702221188ed",
            "picture": "https://cdn.drukarnia.com.ua/64807c9afb6c8702221188ed/images/articles/preview/D5UX5Pe2DLkdp-nRdVq.jpeg",
            "mainTag": "Рецензії",
            "readTime": 129,
            "slug": "teneta-viini-pavlo-derev-yanko-p0F0K",
            "mainTagSlug": "recenziyi",
            "mainTagId": "64204eacb4306ff6ba8c6c5b",
            "createdAt": "2023-12-30T07:09:25.269Z",
            "isBookmarked": False
        },
        {
            "id_": "656ddde5c1d4e0d80e67e607",
            "title": "Аркан вовків — Павло Деревʼянко",
            "description": "Перша книга з циклу “Літопис Сірого Ордену” done. Я мала вищі очікування, бо твір називають одним з кращих в українському фентезі. Не було ВАУ, але твір твердо сподобався. Залишився приємний післясмак і кілька ниточок інтриги, що вестимуть мене далі вовчою стежкою.",
            "owner": "64807c9afb6c8702221188ed",
            "picture": "https://cdn.drukarnia.com.ua/64807c9afb6c8702221188ed/images/articles/preview/PVKaawSQB52564-pn9r.jpeg",
            "mainTag": "Павло Дерев'янко",
            "readTime": 215,
            "slug": "arkan-vovkiv-pavlo-derev-yanko-2rnDJ",
            "mainTagSlug": "pavlo-derev-yanko",
            "mainTagId": "656ddde57d851addfd63dbae",
            "createdAt": "2023-12-04T14:10:46.449Z",
            "isBookmarked": False
        }
    ],
    "content": {
        "id_": "65aac36c2e16847e21eb63c8",
        "json": {
            "type": "doc",
            "content": [
                {
                    "type": "title",
                    "content": [
                        {
                            "type": "text",
                            "text": "Пісня дібров — Павло Дерев'янко"
                        }
                    ]
                },
                {
                    "type": "figure",
                    "attrs": {
                        "src": "https://cdn.drukarnia.com.ua/64807c9afb6c8702221188ed/images/articles/65aac1b22e16847e21eb5d0d/DzN6391654.37727492437.jpeg",
                        "alt": None,
                        "title": None,
                        "secondarySrc": "https://cdn.drukarnia.com.ua/64807c9afb6c8702221188ed/images/articles/65aac1b22e16847e21eb5d0d/DzN6391654.37727492437.webp",
                        "width": 700,
                        "height": 524,
                        "loading": "eager"
                    }
                },
                {
                    "type": "paragraph",
                    "content": [
                        {
                            "type": "text",
                            "text": "Вовча стежка, що вела героїв понад 10 років, добігла кінця. Дуже важко прощатися з направду чудовим, нашим фентезі made in Ukraine. “Пісня дібров” —  третя частина трилогії Litopys Siroho Ordenu — стала розгадкою, ключем до всіх недосказаних, незрозумілих, навмисно прихованих моментів історії характерників."
                        }
                    ]
                },
                {
                    "type": "paragraph",
                    "content": [
                        {
                            "type": "text",
                            "text": "Коли я бралася її читати, очікувала зовсім іншого. Здивувалася, що Темуджина вбили на самому початку. Про що йтиметься далі? Уявляла, як герої битимуться за землі Гетьманату, а тоді зійдуться в нерівному бою з істотами Потойбіччя. Припускала, що Северин ковтне всесильний смарагд, щоб кинути виклик Володарці. Думала, що Орден відродиться з попелу, а Буда знову прийматиме галасливе товариство характерників і джур. Але сталося інакше. Автор розвернув історію на 180 градусів, зробив її дуже особистою історією месників, при цьому навіть більш масштабною в розрізі часів та епох, ніж я могла уявити."
                        }
                    ]
                },
                {
                    "type": "paragraph",
                    "content": [
                        {
                            "type": "text",
                            "text": "Товстунець на 600 сторінок — синергія чудового стилю автора і приголомшливого сюжету. Як написав Дерев'янко в післямові, за задумом, кожна частина мала перевершувати попередню. Йому це вдалося.  "
                        }
                    ]
                },
                {
                    "type": "paragraph",
                    "content": [
                        {
                            "type": "text",
                            "text": "Інколи події в книзі була надміру жорстокими або занадто відвертими. Чого лише вартує страта “божих воїнів” на палях. Та смерть чигає тут не лише на поганців. Разом із книгою завершуються лінії життя багатьох героїв, що стали для читача рідними. Щойно автор розкрив минуле персонажа, щойно дав прочитати його потаємні  думки, як приходив час прощатися."
                        }
                    ]
                },
                {
                    "type": "paragraph",
                    "content": [
                        {
                            "type": "text",
                            "text": "Не знаю, скільки разів сльози не давали дочитати сторінку. Плакала за Катрею, яка рятувала доньку ціною життя. Відчувала щем від загибелі зграї вовків разом із альбіносом Максимом. Проводила сумні паралелі з війною вигаданою та війною реальною, і душа боліла за Київ в оточенні ординців. Сумувала за улюбленим героєм — Пилипом, який пішов на героїчну самопожертву, щоб врятувати країну і нарешті вбити Звіра в собі. "
                        }
                    ]
                },
                {
                    "type": "paragraph",
                    "content": [
                        {
                            "type": "text",
                            "text": "Фінал перевершив очікування. Настав час героям і читачам дізнатися справжню історію походження Ордену характерників. Не ту, яку зелені джури чують від осавул та вчителів. Северин, Гнат і Ярема дізнаються правду з вуст того, хто особисто знав характерника Мамая, хто власноруч створив із нього першого перевертня. Настав час змиритися, що загибель Ордену неминуча і навіть логічна. Настав час зняти прокляття та знищити сувій з кривавими підписами."
                        },
                        {
                            "type": "hardBreak"
                        }
                    ]
                }
            ]
        },
        "owner": "64807c9afb6c8702221188ed",
        "v__": 0
    },
    "isLiked": 0,
    "owner": {
        "id_": "64807c9afb6c8702221188ed",
        "name": "Катерина Василенкова",
        "avatar": "https://lh3.googleusercontent.com/a/AAcHTteUpqaQO-Mbf1GBKskUhz_o2ogDnRgLAoh1teEW=s96-c",
        "descriptionShort": "Веду блог про книжки",
        "followingNum": 17,
        "followersNum": 8,
        "readNum": 423,
        "username": "katerynav",
        "createdAt": "2023-06-07T12:48:26.571Z",
        "socials": {
            "website": "https://goodreads.com/user/show/156950428"
        },
        "donateUrl": "https://www.buymeacoffee.com/kvasylenkox"
    },
    "isBookmarked": False,
    "relationships": {
        "isSubscribed": False,
        "isBlocked": False
    },
    "recommendedArticles": [
        {
            "id_": "64f5e312280f44210243725c",
            "title": "Закінчила писати книгу",
            "description": "Давненько мене тут не було. Утім, повернулася я не з пустими руками — я дописала першу книгу трилогії “Мольфаріум”. Офіційно.",
            "thumbPicture": "https://cdn.drukarnia.com.ua/64c80d78280f442102151fe9/images/articles/preview/VbeVP9mg2lEtrHPmR79.webp",
            "mainTag": "Письменництво",
            "tags": [
                "64206950b4306ff6baf8cadb",
                "63d714e84b15077ac00bb245",
                "643fde5f216b1e38e2e998e4",
                "643d5b96665d056f2cc76d66",
                "645059f8d95767b9e124eaad"
            ],
            "sensitive": False,
            "canonical": None,
            "likeNum": 13,
            "commentNum": 0,
            "readTime": 71,
            "slug": "zakinchila-pisati-knigu-Xeh0R",
            "mainTagSlug": "pismennictvo",
            "mainTagId": "64206950b4306ff6baf8cadb",
            "createdAt": "2023-09-04T14:00:51.445Z",
            "owner": {
                "id_": "64c80d78280f442102151fe9",
                "name": "Лія Гако",
                "avatar": "https://cdn.drukarnia.com.ua/64c80d78280f442102151fe9/images/8_r7avatar.jpeg",
                "username": "lia_gako",
                "descriptionShort": "художниця слова",
                "followingNum": 14,
                "followersNum": 11,
                "readNum": 276,
                "createdAt": "2023-07-31T19:37:28.755Z",
                "socials": {
                    "twitter": "https://twitter.com/lia_gako",
                    "instagram": "https://instagram.com/lia.gako/",
                    "facebook": "https://facebook.com/profile.php?id=100094421545735",
                    "tiktok": "https://tiktok.com/@lia_gako",
                    "youtube": "https://youtube.com/@liagako_asmr",
                    "website": "https://liagako.wixsite.com/molfarium"
                }
            },
            "isBookmarked": False
        },
        {
            "id_": "64ca1d84280f44210216afe6",
            "title": "Запрошую у текстову рольову гру!",
            "description": "Довгоочікувана подія! 💔Текстова рольова гра за мотивами \"Мольфаріуму\" — українського підліткового фентезі — офіційно відкрита! ✨ Створіть власного персонажа, напишіть свою історію та  пориньте у світ магії",
            "thumbPicture": "https://cdn.drukarnia.com.ua/64c80d78280f442102151fe9/images/articles/preview/YGzinLqPSlOBFs5xQEW.webp",
            "mainTag": "Рольова Гра",
            "tags": [
                "643b2a957d4bade1314e0e88",
                "644e837ad95767b9e1b5be6f",
                "64512710d95767b9e12e39e8",
                "63d714e84b15077ac00bb245",
                "64206950b4306ff6baf8cadb"
            ],
            "sensitive": False,
            "canonical": None,
            "likeNum": 24,
            "commentNum": 5,
            "readTime": 47,
            "slug": "zaproshuyu-u-tekstovu-rolovu-gru-fhn2Z",
            "mainTagSlug": "rolova-gra",
            "mainTagId": "643b2a957d4bade1314e0e88",
            "createdAt": "2023-08-02T09:10:29.233Z",
            "owner": {
                "id_": "64c80d78280f442102151fe9",
                "name": "Лія Гако",
                "avatar": "https://cdn.drukarnia.com.ua/64c80d78280f442102151fe9/images/8_r7avatar.jpeg",
                "username": "lia_gako",
                "descriptionShort": "художниця слова",
                "followingNum": 14,
                "followersNum": 11,
                "readNum": 276,
                "createdAt": "2023-07-31T19:37:28.755Z",
                "socials": {
                    "twitter": "https://twitter.com/lia_gako",
                    "instagram": "https://instagram.com/lia.gako/",
                    "facebook": "https://facebook.com/profile.php?id=100094421545735",
                    "tiktok": "https://tiktok.com/@lia_gako",
                    "youtube": "https://youtube.com/@liagako_asmr",
                    "website": "https://liagako.wixsite.com/molfarium"
                }
            },
            "isBookmarked": False
        },
        {
            "id_": "64856c78280f442102d286ee",
            "title": "Крутозварений",
            "description": "Боже, скільки тут адаптованих написів в антуражі! Ця титанічна уважність і майстерність ретушера варті поваги!",
            "thumbPicture": "https://cdn.drukarnia.com.ua/643e441fafa9d4573a00f641/images/articles/preview/9nFZXBDhcx6kXqeOGqv.webp",
            "mainTag": "Комікси",
            "tags": [
                "644932452948bacadbc006ea",
                "6447c8390f97e4426ae349c2",
                "643c73edcda8bb95f9a1f38c",
                "64202ea1b4306ff6ba012e36",
                "64204eacb4306ff6ba8c6c5b"
            ],
            "sensitive": False,
            "canonical": "https://ueartemis.wordpress.com/2022/01/25/hardboiled/",
            "likeNum": 0,
            "commentNum": 0,
            "readTime": 47,
            "slug": "krutozvarenii-u0AIh",
            "mainTagSlug": "komiksi",
            "mainTagId": "644932452948bacadbc006ea",
            "createdAt": "2023-06-11T06:40:57.928Z",
            "owner": {
                "id_": "643e441fafa9d4573a00f641",
                "name": "М. М. Безрук",
                "avatar": "https://cdn.drukarnia.com.ua/643e441fafa9d4573a00f641/images/T8Vjavatar.png",
                "username": "UeArtemis",
                "followingNum": 8,
                "followersNum": 30,
                "readNum": 3609,
                "createdAt": "2023-04-18T07:17:51.516Z",
                "socials": {
                    "twitter": "https://twitter.com/UeArtemis",
                    "facebook": "https://facebook.com/ueartemis",
                    "website": "https://arkush.net/user/853"
                },
                "donateUrl": "https://donatello.to/ueartemis",
                "descriptionShort": "Аматор мовознавства"
            },
            "isBookmarked": False
        }
    ],
    "comments": []
}

    article = ArticleModel(**data)
    articles = article.authorArticles
    print(articles[0].owner)
