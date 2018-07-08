# -*- coding: utf-8 -*-
'''
@author  : smh2208
@software: PyCharm
@file    : test.py
@time    : 2018/6/25 20:21
@desc    :
'''

s = '''
<li id="note-29866089" data-note-id="29866089" class="">
  <div class="content">
    <a class="title" target="_blank" href="/p/c738ff7a26cd">你太优秀，我不想和你做朋友了</a>
    <p class="abstract">
      1 前几天和一个以前玩得很好的朋友发消息，我说，我们俩好久没聊天了呀！她许久没有回复，我就像以前一样发去了一堆表情包。 可能是实在烦了，她回了一...
    </p>
    <div class="meta">
      <a class="nickname" target="_blank" href="/u/4ff85d9e8b94">三川呐</a>
        <a target="_blank" href="/p/c738ff7a26cd#comments">
          <i class="iconfont ic-list-comments"></i> 16
</a>      <span><i class="iconfont ic-list-like"></i> 24</span>
    </div>
  </div>
</li>'''

from lxml.html import etree

