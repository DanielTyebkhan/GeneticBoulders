import structs
import ribs_interface
import constants

if __name__ == '__main__':
    params = structs.MEParams(
        (10, 10), [(constants.MOONBOARD_COLUMNS, constants.MOONBOARD_ROWS)])
    ribs_interface.run_mapelites(params))