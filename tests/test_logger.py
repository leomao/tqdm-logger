from tqdm import tqdm
from tqdm import trange
from time import sleep
from tqdm_logger import logger
from tqdm_logger import seclog, log, atten, note, warning
from tqdm_logger.ansistyle import stylize, fg, bg, attr, RESET

def test_main():
    print(stylize('TESTING', attr('underlined')))
    logger.info(stylize('TESTING', fg('green'), attr('underlined')))
    for i in trange(10):
        logger.warning(f'TEST {i}')
    logger.debug(atten(f'ENDING'))
    logger.debug(123)

    with tqdm(total=10) as tbar:
        for i in range(10):
            seclog(['Graph', 'blue'], 123)
            seclog(['Graph', 'blue'])
            warning('this is a warning\nsomething wrong')
            log('multiline logging:\nthis is a multiline string')
            log(note('hao', 123))
            sleep(0.2)
            tbar.update(1)

if __name__ == '__main__':
    test_main()
