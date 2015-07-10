try:
    #let's try Pillow
    from PIL import Image
except ImportError:
    #not Pillow => you're using PIL. You should upgrade, but it's your choice.
    import Image
