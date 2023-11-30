import kerning_fea
import banner_atlas
import create_font
import create_svgs
import test_font


if __name__ == "__main__":
    print("Creating banner atlas")
    banner_atlas.create()
    print("Extract and convert svgs")
    create_svgs.recreate()
    print("Inject feature file")
    kerning_fea.write_fea()
    print("Create font")
    create_font.call()
    print("Run tests")
    test_font.test()
    print("Success")
