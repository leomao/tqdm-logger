import random
from tqdm import tqdm
from tqdm import trange
from time import sleep
import tqdmlogger as logger
from tqdmlogger import seclog, log, atten, note, warning
from tqdmlogger.ansistyle import stylize, fg, bg, attr, RESET


def test_main():
    print(stylize('TESTING', attr('underlined')))
    logger.logger.info(stylize('info TESTING', fg('green'), attr('underlined')))
    logger.logger.info(stylize('info logging', fg('red'), attr('bold')))
    logger.log(stylize('TESTING', fg('green'), attr('underlined')))
    logger.log(stylize('logging', fg('red'), attr('bold')))
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

    logger.set_high_precision(True)

    for i in trange(10):
        ha = 'ha' * (9 - i)
        logger.seclog(['Testing', 'red'], 'TEST: {}'.format(ha), update=True)
        sleep(0.2)

    logger.set_time_mode('time')

    for i in trange(10):
        ha = 'ha' * (9 - i)
        value = random.random()
        logger.seclog(['Multiline', 'yellow'],
                      'something: {}\ncool: {}'.format(ha, value), update=True)
        sleep(0.2)

    logger.set_time_mode('delta')

    for i in trange(10):
        ha = 'ha' * (9 - i)
        value = random.random()
        logger.seclog(['Multiline', 'yellow'],
                      'something: {}\ncool: {}'.format(ha, value), update=True)
        if (i % 3) == 0:
            logger.flush()
        sleep(0.2)

    for i in trange(10):
        with logger.updating():
            ha = 'ha' * (9 - i)
            value = random.random()
            logger.seclog(['Context', 'cyan'], 'something: {}'.format(ha))
            logger.seclog(['Context', 'cyan'], 'nice: {}'.format(value))
            sleep(0.2)




if __name__ == '__main__':
    test_main()
