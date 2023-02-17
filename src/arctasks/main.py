"""
< name: arc-tasks >
< author: Predrag Bunic >
< contact: noctdruid@proton.me >
< source: github.com/noctdruid/arc-tasks >
< license: GPL v3 >
"""

from arctasks.interface import Interface


def init():
    Interface().initialize_args()