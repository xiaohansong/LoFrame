"""
The MIT License (MIT)

Copyright (c) <2015> <Xiaohan Song>

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

"""
from core.connector import Connector
from core.responser import Responser
from core.daemon import Clean
import logging
import sys

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s:%(filename)s %(levelname)s %(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S',
                    filename='loframe.log',
                    filemode='w')

if __name__ == "__main__":
	conn = Connector()
	conn.start()
	rep = Responser()
	rep.start()
	clean = Clean()
	clean.start()
