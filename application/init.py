import os

from application import controller

from checkio_taker.config import configure as checkio_configure
from memoplat.config import configure as memoplat_configure
from m_covers.config import configure as m_covers_configure


def configure():
    memoplat_configure(os.path.join(os.path.dirname(os.path.dirname(__file__)),
                                    'storage', 'memoplat.sqlite'))
    m_covers_configure(os.path.join(os.path.dirname(os.path.dirname(__file__)),
                                    'storage', 'm_covers.sqlite'))
    checkio_configure(os.path.join(os.path.dirname(os.path.dirname(__file__)),
                                   'storage', 'checkio.sqlite'))


if __name__ == '__main__':
    configure()
    controller.app.run()
