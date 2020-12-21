from basis import *

def needJump(deltax, deltah):
    if deltah > 0:
        return True
    return deltax > (2*deltah/G)**0.5 * ENEMYSPEED

class EnemyVI:
    def track(self):
        # follow palyer
        # -1 for left, 1 for right, 0 for stop
        
        # at the same stage
        if self.standOn == list_player[0].standOn:
            if self.box.x >= list_player[0].box.xr:
                return -1
            elif self.box.xr <= list_player[0].box.x:
                return 1
            return 0
        
        else:
            goto = list_platform[self.standOn].route[list_player[0].standOn]
            # overlap
            if list_platform[self.standOn].rect_l <= list_platform[goto].rect_r and list_platform[self.standOn].rect_r >= list_platform[goto].rect_l:
                if self.box.centerx < list_platform[goto].rect_l:
                    return 1
                elif self.box.centerx > list_platform[goto].rect_r:
                    return -1
                else :
                    if list_platform[self.standOn].rect_t >= list_platform[goto].rect_t:
                        self.jumpdown()
                    elif list_platform[self.standOn].rect_t < list_platform[goto].rect_t:
                        self.jump()
                    return 0
            # towards left
            elif list_platform[self.standOn].rect_l > list_platform[goto].rect_r:
                if self.box.centerx <= list_platform[self.standOn].rect_l and needJump(list_platform[self.standOn].rect_l-list_platform[goto].rect_r, list_platform[goto].rect_t-list_platform[self.standOn].rect_t):
                    self.jump()
                if self.box.centerx <= list_platform[goto].rect_l:
                    return 0
                return -1
            # towards right
            elif list_platform[self.standOn].rect_r < list_platform[goto].rect_l:
                if self.box.centerx >= list_platform[self.standOn].rect_r and needJump(list_platform[self.standOn].rect_r-list_platform[goto].rect_l, list_platform[goto].rect_t-list_platform[self.standOn].rect_t):
                    self.jump()
                if self.box.centerx >= list_platform[goto].rect_l:
                    return 0
                return 1
            return 0
