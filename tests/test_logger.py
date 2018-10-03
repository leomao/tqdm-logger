import random
from tqdm import tqdm
from tqdm import trange
from time import sleep
import tqdm_logger as logger
from tqdm_logger import seclog, log, atten, note, warning
from tqdm_logger.ansistyle import stylize, fg, bg, attr, RESET


def test_main():
    print(stylize('TESTING', attr('underlined')))
    logger.logger.info(stylize('TESTING', fg('green'), attr('underlined')))
    for i in trange(10):
        logger.logger.warning('TEST {}'.format(i))
        sleep(0.1)
    logger.logger.debug(atten('ENDING'))
    logger.logger.debug(123)

    with tqdm(total=10) as tbar:
        for i in range(10):
            logger.seclog(['Graph', 'blue'], 123)
            logger.seclog(['Graph', 'blue'])
            warning('this is a warning\nsomething wrong')
            logger.log('multiline logging:\nthis is a multiline string')
            logger.log(note('hao', 123))
            sleep(0.2)
            tbar.update(1)

    for i in trange(10):
        ha = 'ha' * (9 - i)
        logger.seclog(['Testing', 'red'], 'TEST: {}'.format(ha), update=True)
        sleep(0.2)

    # if use multiple updating log
    logger.reset()
    for i in trange(10):
        ha = 'ha' * (9 - i)
        value = random.random()
        logger.seclog(['Multiline', 'yellow'],
                      'something: {}\ncool: {}'.format(ha, value), update=True)
        sleep(0.2)


if __name__ == '__main__':
    test_main()
