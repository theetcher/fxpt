import maya.cmds as m
import pymel.core as pm


SCRIPT_NAME = 'FX Reorient'
WIN_NAME = 'fx_reorientWin'

BUTTON_WIDTH = 150
MAIN_BUTTONS_HEIGHT = 30

LOCATOR_FLY_AWAY_DISTANCE = 100

win = None


#noinspection PyAttributeOutsideInit
#noinspection PyMethodMayBeStatic
#noinspection PyUnusedLocal
class ReorientUI(object):
    def __init__(self):
        self.processor = OrientProcessor()
        self.ui_create()
        self.initial_object_setup()
        self.ui_refresh()

    def ui_create(self):

        self.ui_close()

        self.window = pm.window(
            WIN_NAME,
            title=SCRIPT_NAME,
            maximizeButton=False
        )

        with self.window:
            with pm.formLayout() as ui_lay_main_form:
                with pm.scrollLayout(childResizable=True) as ui_lay_main_scroll:
                    with pm.columnLayout(adjustableColumn=True):
                        with self.create_frame('Manual Orient', collapsed=True):
                            with pm.columnLayout(adjustableColumn=True, columnOffset=('both', 2)):
                                pm.separator(style='none', height=5)

                                self.ui_btn_create_tripod = pm.button(
                                    label='Create Tripod',
                                    height=MAIN_BUTTONS_HEIGHT,
                                    command=self.on_btn_create_tripod
                                )

                                pm.separator(style='none', height=5)

                        with self.create_frame('Automatic Orient'):
                            with pm.columnLayout(adjustableColumn=True, columnOffset=('both', 2)):
                                with self.create_button_text_field_row_layout():
                                    self.ui_btn_set_object = pm.button(
                                        label='Set Object',
                                        command=self.on_btn_set_object_clicked
                                    )
                                    self.ui_txtfld_object_name = pm.textField(editable=False)

                                with self.create_button_text_field_row_layout():
                                    self.ui_btn_set_pivot_vtx = pm.button(
                                        label='Set Pivot',
                                        command=self.on_btn_set_pivot_vtx_clicked
                                    )
                                    self.ui_txtfld_pivot_vtx = pm.textField(editable=False)

                                with self.create_button_text_field_row_layout():
                                    self.ui_btn_set_aim_vtx = pm.button(
                                        label='Set Aim',
                                        command=self.on_btn_set_aim_vtx_clicked
                                    )
                                    self.ui_txtfld_aim_vtx = pm.textField(editable=False)

                                with self.create_button_text_field_row_layout():
                                    self.ui_btn_set_up_vtx = pm.button(
                                        label='Set Up',
                                        command=self.on_btn_set_up_vtx_clicked
                                    )
                                    self.ui_txtfld_up_vtx = pm.textField(editable=False)

                                pm.separator(style='none', height=5)

                                with pm.formLayout() as ui_lay_btn_form:
                                    self.ui_btn_reset = pm.button(
                                        label='Reset',
                                        height=MAIN_BUTTONS_HEIGHT,
                                        command=self.on_btn_reset_clicked
                                    )

                                    self.ui_btn_fix_orient = pm.button(
                                        label='Fix Orientation',
                                        height=MAIN_BUTTONS_HEIGHT,
                                        command=self.on_btn_fix_orient
                                    )

                                    ui_lay_btn_form.attachNone(self.ui_btn_reset, 'top')
                                    ui_lay_btn_form.attachForm(self.ui_btn_reset, 'left', 2)
                                    ui_lay_btn_form.attachPosition(self.ui_btn_reset, 'right', 2, 50)
                                    ui_lay_btn_form.attachForm(self.ui_btn_reset, 'bottom', 2)

                                    ui_lay_btn_form.attachNone(self.ui_btn_fix_orient, 'top')
                                    ui_lay_btn_form.attachPosition(self.ui_btn_fix_orient, 'left', 2, 50)
                                    ui_lay_btn_form.attachForm(self.ui_btn_fix_orient, 'right', 2)
                                    ui_lay_btn_form.attachForm(self.ui_btn_fix_orient, 'bottom', 2)

                self.ui_btn_close = pm.button(
                    label='Close',
                    height=MAIN_BUTTONS_HEIGHT,
                    command=self.ui_close
                )

                ui_lay_main_form.attachForm(ui_lay_main_scroll, 'top', 2)
                ui_lay_main_form.attachForm(ui_lay_main_scroll, 'left', 2)
                ui_lay_main_form.attachForm(ui_lay_main_scroll, 'right', 2)
                ui_lay_main_form.attachControl(ui_lay_main_scroll, 'bottom', 2, self.ui_btn_close)

                ui_lay_main_form.attachNone(self.ui_btn_close, 'top')
                ui_lay_main_form.attachForm(self.ui_btn_close, 'left', 2)
                ui_lay_main_form.attachForm(self.ui_btn_close, 'right', 2)
                ui_lay_main_form.attachForm(self.ui_btn_close, 'bottom', 2)

    def create_button_text_field_row_layout(self):
        return pm.rowLayout(
            numberOfColumns=2,
            adjustableColumn=2,
            columnWidth=(1, BUTTON_WIDTH),
            columnAttach=(1, 'both', 2)
        )

    def create_frame(self, name, collapsed=False):
        return pm.frameLayout(
            label=name,
            collapsable=True,
            marginHeight=3,
            borderStyle='etchedIn',
            borderVisible=True,
            collapse=collapsed
        )

    def ui_refresh(self):
        ori_data_object, ori_data_pivot_vtx, ori_data_aim_vtx, ori_data_up_vtx = self.processor.get_ori_data_strings()
        self.ui_txtfld_object_name.setText(ori_data_object)
        self.ui_txtfld_pivot_vtx.setText(ori_data_pivot_vtx)
        self.ui_txtfld_aim_vtx.setText(ori_data_aim_vtx)
        self.ui_txtfld_up_vtx.setText(ori_data_up_vtx)

        self.ui_btn_fix_orient.setEnable(self.processor.is_valid_setup())

    def initial_object_setup(self):
        self.processor.set_working_data_initially()
        self.ui_refresh()

    def on_btn_set_object_clicked(self, *args):
        if self.processor.set_object():
            self.ui_refresh()
        else:
            simple_warning('Select one transform or joint.')

    def on_btn_set_pivot_vtx_clicked(self, *args):
        if self.processor.set_pivot_vtx():
            self.ui_refresh()
        else:
            simple_warning('Select one transform or polygon vertex.')

    def on_btn_set_aim_vtx_clicked(self, *args):
        if self.processor.set_aim_vtx():
            self.ui_refresh()
        else:
            simple_warning('Select one transform or polygon vertex.')

    def on_btn_set_up_vtx_clicked(self, *args):
        if self.processor.set_up_vtx():
            self.ui_refresh()
        else:
            simple_warning('Select one transform or polygon vertex.')

    def on_btn_reset_clicked(self, *args):
        self.processor.init_data()
        self.ui_refresh()

    def on_btn_fix_orient(self, *args):
        self.processor.fix_orient()

    def on_btn_create_tripod(self, *args):
        self.processor.create_tripod()

    def ui_close(self, *args):
        if pm.window(WIN_NAME, exists=True):
            pm.deleteUI(WIN_NAME, window=True)


#TODO: to get rid of three vtx fields and functions and repeating code need to put all this data in dict.
# there will be only one function "set_vtx" with parameter which vertex to setup
# parameter should be represented by static variables in OrientProcessor

#noinspection PyAttributeOutsideInit
#noinspection PyMethodMayBeStatic
class OrientProcessor(object):

    def __init__(self):
        self.init_data()

    def init_data(self):
        self.ori_data_object = None
        self.ori_data_pivot_vtx = None
        self.ori_data_aim_vtx = None
        self.ori_data_up_vtx = None

    def get_ori_data_strings(self):
        return (
            str(self.ori_data_object),
            str(self.ori_data_pivot_vtx),
            str(self.ori_data_aim_vtx),
            str(self.ori_data_up_vtx)
        )

    def set_working_data_initially(self):
        self.set_object()
        self.set_pivot_vtx()

    def set_object(self):
        res = self.get_working_object_from_selection(force_transform=True)
        if res:
            self.ori_data_object = res
            return True
        return False

    def set_pivot_vtx(self):
        res = self.get_working_object_from_selection()
        if res:
            self.ori_data_pivot_vtx = res
            return True
        return False

    def set_aim_vtx(self):
        res = self.get_working_object_from_selection()
        if res:
            self.ori_data_aim_vtx = res
            return True
        return False

    def set_up_vtx(self):
        res = self.get_working_object_from_selection()
        if res:
            self.ori_data_up_vtx = res
            return True
        return False

    def get_working_object_from_selection(self, force_transform=False):

        selection = m.ls(selection=True, long=True, flatten=True)

        if len(selection) != 1:
            return None

        selection = selection[0]
        component_selected = '.' in selection
        node = selection.split('.')[0]

        if component_selected and self.is_mesh_transform(node):
            if force_transform:
                return node
            else:
                return selection

        if m.nodeType(node) in ('transform', 'joint'):
            return node
        else:
            return None

    def get_parent(self, node):
        parents = m.listRelatives(node, fullPath=True, parent=True)
        if parents is None:
            return None
        else:
            return parents[0]

    def is_mesh_transform(self, node):
        for child in m.listRelatives(node, fullPath=True, children=True):
            if m.nodeType(child) == 'mesh':
                return True
        return False

    def is_valid_setup(self):
        return not any([data_field is None for data_field in
                        self.ori_data_object,
                        self.ori_data_pivot_vtx,
                        self.ori_data_aim_vtx,
                        self.ori_data_up_vtx
                        ])

    def fix_orient(self):
        selected_objects = m.ls(sl=True, l=True, fl=True)

        tri_pivot, tri_aim, tri_up, aim_constraint = self.create_tripod()

        x, y, z = self.get_world_space_coords(self.ori_data_pivot_vtx)
        m.move(x, y, z, tri_pivot, absolute=True)
        x, y, z = self.get_world_space_coords(self.ori_data_aim_vtx)
        m.move(x, y, z, tri_aim, absolute=True)
        x, y, z = self.get_world_space_coords(self.ori_data_up_vtx)
        m.move(x, y, z, tri_up, absolute=True)

        parent_constraint = m.parentConstraint(
            tri_pivot,
            self.ori_data_object,
            maintainOffset=True
        )[0]

        pivot_x, pivot_y, pivot_z = m.xform(tri_pivot, q=True, ws=True, t=True)
        m.move(pivot_x, pivot_y, pivot_z + LOCATOR_FLY_AWAY_DISTANCE, tri_aim, absolute=True)
        m.move(pivot_x, pivot_y + LOCATOR_FLY_AWAY_DISTANCE, pivot_z, tri_up, absolute=True)

        m.delete((parent_constraint, aim_constraint, tri_pivot, tri_aim, tri_up))

        if selected_objects:
            m.select(selected_objects)
        else:
            m.select(cl=True)

    def create_tripod(self):
        tri_pivot = m.spaceLocator(name='tri_pivot')[0]
        tri_aim = m.spaceLocator(name='tri_aim')[0]
        m.move(0, 0, 1, tri_aim, absolute=True)
        tri_up = m.spaceLocator(name='tri_up')[0]
        m.move(0, 1, 0, tri_up, absolute=True)

        constraint = m.aimConstraint(
            tri_aim,
            tri_pivot,
            worldUpType='object',
            worldUpObject=tri_up
        )[0]

        return tri_pivot, tri_aim, tri_up, constraint

    def get_world_space_coords(self, ori_obj):
        # watch(ori_obj, 'ori_obj')
        if '.' in ori_obj:
            return m.pointPosition(ori_obj, world=True)
        else:
            return m.xform(ori_obj, q=True, rp=True, ws=True)


def run():
    global win
    win = ReorientUI()


#----------------------------------------------------------------------------------------------------------------------
# Helper Functions
#----------------------------------------------------------------------------------------------------------------------

def simple_warning(message):
    pm.confirmDialog(
        title=SCRIPT_NAME,
        message=message,
        button=['Ok']
    )