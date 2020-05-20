import pygame
import math


def main():

    Maru().play_pygame()
    print("Thanks for playing!")
    print("\nSource for Financial Tip: Statistics Canada.  Table  37-10-0036-01   National"
          " graduates survey, student debt from all sources, by province and level of study")


class Maru:  # Maru is the interactable interface

    def __init__(self):
        pygame.init()
        self.window = pygame.display.set_mode([640, 480])
        pygame.display.set_caption('Talk to Maru')
        self.white = (255, 255, 255)
        self.black = (0,0,0)
        self.font = pygame.font.SysFont('consolas', 18, True)
        self.user = User(self.window)
        self.turn = 0  # pointer for which dialogue to be printed
        self.running = True
        self.name = ''  # first input
        self.yourday = ''  # hows ur day? input
        self.input = ''  # other inputs
        self.dial_opt = 0 # which list of talks to talk of
        self.dialogue()  # initialized talks
        self.t_len = len(self.listOtalks[0])
        self.lines = 0 # number of lines for maru's dialogue


    def play_pygame(self): # runs pygame settings along with displays

        text =''

        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == pygame.KEYDOWN:  # every situation where user has to type something on keyboard
                    if self.dial_opt == 0:  # until when user has to select tips
                        if event.key == pygame.K_RETURN and self.turn != 4:  # 5th slide doesn't take enter
                            if self.turn == 0:
                                self.name = text
                            elif self.turn == 2:
                                self.yourday = text
                                self.textChange()
                            self.input = text
                            text = ''
                            self.update()
                        elif event.key == pygame.K_BACKSPACE:
                            text = text[:-1]
                        elif event.key == pygame.K_ESCAPE and self.turn == self.t_len-1:  # last page; press ESC to quit
                            self.running = False
                        elif self.turn == 4:
                            if event.key == pygame.K_1:
                                self.turn = 0
                                self.dial_opt = 1
                            elif event.key == pygame.K_2:
                                self.turn += 1
                        elif not self.turn == self.t_len-1:  # don't take text input on last slide
                            text += event.unicode
                    elif self.dial_opt == 1:
                        if event.key == pygame.K_1:
                            self.dial_opt = 2
                        elif event.key == pygame.K_2:
                            self.dial_opt = 3
                        elif event.key == pygame.K_3:
                            self.dial_opt = 4
                        elif event.key == pygame.K_ESCAPE:
                            self.turn = self.t_len-1
                            self.dial_opt = 0
                    elif self.dial_opt > 1:
                        if event.key == pygame.K_1:  # next page
                            self.update()
                        if self.turn > 0 and event.key == pygame.K_2:  # back page
                            self.turn -= 1
                        # ESC on last page means return to selection
                        if self.turn == len(self.listOtalks[self.dial_opt])-1 and event.key == pygame.K_ESCAPE:
                            self.turn = 0
                            self.dial_opt = 1

            self.window.fill(self.black)
            self.draw_Maru()
            self.user.draw()
            self.Maru_talk()
            self.user.user_input(text,self.turn,self.dial_opt)

            pygame.display.flip()

    def Maru_talk(self):

        strt = [100, 30]  # starting point of talk bubble
        height = self.window.get_height()/5  # height of bubble
        width = self.window.get_width()/3  # width of bubble
        maxC = 20  # max number of char each line

        talk = self.dialogue() # max width of text = 25 char

        manystars = talk.count('*')  # how many *'s?
        # * in dialogue indicates the need for new space (b/c \n doesn't work when rendering text)
        # if I detect *, fill the rest of the line with whitespaces
        for i in range(manystars):
            space = ' '*(maxC-(talk.find('*')%20))  # (max character for the line - remainder of space after *)
            talk = talk.replace("*",space,1)

        txt_w = len(talk)  # width of text counted in # of characters
        txt_h = self.font.get_height()  # height counted in pixels

        # number of lines = (number of characters / max characters for each line) rounded up
        self.lines = math.ceil(txt_w/maxC)
        texts = [talk[i:i + maxC] for i in range(0, txt_w, maxC)]  # new line every 20 char

        for each_line in range(self.lines):  # displays each line of TEXTS

            text = self.font.render(texts[each_line], True, self.white)  # renders each line

            txt_x = strt[0] + 7  # co-ordinate for beginning of text
            txt_y = strt[1] + 5 + txt_h*each_line  # y co-ordinate adjusted according to number of lines

            textRect = text.get_rect()
            textRect.center = (txt_x,txt_y)
            self.window.blit(text, (txt_x,txt_y))

        if self.lines <= 4:  # adjusting y co-ords of bottom 2 lines of text bubble
            final_lines = (width+strt[0], height+strt[1]),(strt[0], height + strt[1])
        else:
            extra_lines = (self.lines - 4) * txt_h
            final_lines = (width+strt[0], height+strt[1]+extra_lines),(strt[0], height + strt[1]+extra_lines)

        pygame.draw.aalines(self.window, self.white, True,  # draw dialogue_bubble
                            (strt, (width+strt[0], strt[1]), (width+strt[0], 3*height/5+strt[1]),
                         (width+strt[0]+50, height+strt[1]+35),final_lines[0],final_lines[1]
                         ))

    def textChange(self):  # change self.yourday input to 2nd person narrative
        if 'my' in self.yourday.lower() or 'i ' in self.yourday.lower():
            self.yourday = self.yourday.replace('my','your')
            self.yourday = self.yourday.replace('i ','you ')
            self.yourday = self.yourday.replace('My','Your')
            self.yourday = self.yourday.replace('I ','You ')

    def dialogue(self):  # adjust content of self.talk
        self.listOtalks =[  # Don't use \ for dialogue string; use " instead of ' if necessary
                    # -------------------- < 20 char
                    ["Howdy? My name is*"
                     "Maru! What's yours?",
                     'Nice to meet you*%s!*'
                     'Can you tell meow*'
                     'about your day?' % self.input,
                     'You had a(n) %s '
                     'day hey?*'
                     'What made you feel*'
                     'that way?' % self.input,
                     '%s? I see.*'
                     'Thank you for telling me, %s :3' % (self.yourday,self.name),
                     'Wait! Before you go,'
                     'Do you want some*'
                     'random tips for uni?',
                     'It was nice to meet*'
                     'you %s~*'
                     '(Press ESC to quit)' % self.name],
                    ['Select your tip!*'
                     '1. Financial Tip*'
                     '2. Study Tip*'
                     '3. Mental Health Tip'
                     'ESC if you are done!'],
                    # -------------------- < 20 char

                    # Financial Tip
                    ['If meow are using*'
                     'student loans,*'
                     'use it wisely!*'
                     '(1 = next)',
                     'Did meow know,*'
                     'average Canadian st-'
                     'udents who take out*'
                     'student loans are*'
                     '$26,300 in debt by*'
                     'the time they gradu-'
                     'ate?*'
                     '(1 = next, 2 = back)',
                     'That means, even wi-'
                     'thout interest, you '
                     'would have to pay b-'
                     'ack $438 every month'
                     'for 5 year!*'
                     '(1 = next, 2 = back)',
                     "With interest (let's"
                     "say with a fixed*"
                     "rate of 7%), even if"
                     "you pay in time*"
                     "every month, you wo-"
                     "uld have paid over*"
                     "$5000 just from int-"
                     "erest by the end*"
                     "of 5th year D:*"
                     "(1 = next, 2 = back)",
                     'Also, did you know*'
                     'that student loan*'
                     'interest starts to*'
                     'accumulate as soon*'
                     'as you graduate?*'
                     '(1 = next, 2 = back)',
                     'Common misunderstan-'
                     'ding is that the*'
                     '"Grace Period" that '
                     'students get after*'
                     'graduation is inter-'
                     'est free.*'
                     '(1 = next, 2 = back)',
                     'This is not true!*'
                     'The "Grace Period"*'
                     "just means you don't"
                     "get penalized for*"
                     "not paying the mont-"
                     "hly repayment during"
                     "that period.*"
                     "(1 = next, 2 = back)",
                     "Don't stress too*"
                     "much for now, as you"
                     "will most likely ma-"
                     "ke more money after "
                     "graduating, but just"
                     "keep in mind how you"
                     "spend your loan :^)*"
                     "(1 = next, 2 = back)",
                     'Check output for*'
                     'credits :)*'
                     '(2 = back,*'
                     'ESC = select tips)'],
                    # -------------------- < 20 char

                    # Study Tip
                    ["Be nice to yourself!"
                     "Don't be so strict*"
                     "about everything you"
                     "have to do :)*"
                     "(1 = next)",
                     "Start with what you "
                     "know or can do and*"
                     "give yourself some*"
                     "credit for the work "
                     "you've done.*"
                     "(1 = next, 2 = back)",
                     "After all, you did*"
                     "good! We all know*"
                     "studying doesn't ha-"
                     "ppen without effort."
                     "(1 = next, 2 = back)",
                     "That being said, try"
                     "not to pass on your "
                     "work to yourself of "
                     "tomorrow. If you*"
                     "don't want to do it "
                     "now, you won't want "
                     "to do it tomorrow.*"
                     "(1 = next, 2 = back)",
                     'Lastly,*'
                     'make yourself avail-'
                     'able for school.*'
                     'Make room for recha-'
                     'rging time too. You '
                     'are human, not super'
                     'saiyan!*'
                     '(1 = next, 2 = back)',
                     'Good luck :)*'
                     '(2 = back,*'
                     'ESC = select tips)'],
                    # -------------------- < 20 char

                    # Mental Health Tip
                    ["Mental health is*"
                     "very personal.*"
                     "No one knows exactly"
                     "why you feel the way"
                     "you do. For many,*"
                     "they themselves*"
                     "don't even know!*"
                     "(1 = next)",
                     'Find out why.*'
                     'Whether that means*'
                     'watching Ted Talks*'
                     'on youtube, reading '
                     'self-care books, or '
                     'seeking a therapist.'
                     '(1 = next, 2 = back)',
                     'Reflect on the ideas'
                     'that felt personal*'
                     'to you. The tips I*'
                     'give here are also*'
                     'just what I find ap-'
                     "propriate, but*"
                     "doesn't necessarily "
                     "apply to everyone.*"
                     "(1 = next, 2 = back)",
                     'One big step of bec-'
                     'ming happy, is for*'
                     'you to want to be*'
                     'happy.*'
                     '(1 = next, 2 = back)',
                    # -------------------- < 20 char
                     'Being depressed can '
                     'be addicting as it*'
                     'can be easier to*'
                     'stay as it is than*'
                     'to make an effort to'
                     'change.*'
                     '(This is not meant*'
                     'to be addressed to*'
                     'those who are suffe-'
                     'ring from serious*'
                     'depression)*'
                     '(1 = next, 2 = back)',
                     "Another big step is "
                     "not making yourself "
                     "responsible for oth-"
                     "er people's opinion "
                     "of you.*"
                     "(1 = next, 2 = back)",
                     "Everyone's opinion*"
                     "is very subjective*"
                     "and personal which*"
                     "includes their opin-"
                     "ion of you. Don't*"
                     "blame yourself for*"
                     "their personal*"
                     "matter!*"
                     "(1 = next, 2 = back)",
                    # -------------------- < 20 char
                     'But also keep in*'
                     'mind, people are not'
                     'your enemy to defeat'
                     'rather your ally to '
                     'learn from.*'
                     '(2 = back,*'
                     'ESC = select tips)']]

        talk = self.listOtalks[self.dial_opt][self.turn]
        return talk

    def update(self):  # updates the dialogue turn
        if self.turn < len(self.listOtalks[self.dial_opt])-1:
            self.turn += 1

    def draw_Maru(self):

        Maru_y = int(self.window.get_height()/7*2)  # coordinates of Maru
        Maru_x = int(self.window.get_width()/5*3)
        colorA = (255,203,156)
        colorB = (255,121,3)
        pygame.draw.ellipse(self.window, colorA, (Maru_x,Maru_y,130,75))  # head
        pygame.draw.ellipse(self.window,colorA, (Maru_x+30,Maru_y,70,180))  # body; 30*2+70 = 130 (head's width)
        pygame.draw.polygon(self.window,colorB, ([Maru_x,Maru_y],[Maru_x+30,Maru_y+6],[Maru_x+5,Maru_y+22]))  # left ear
        # left ear points = [x1,y1],[x1+30,y1+6],[x1+5,y1+22]
        # so right ear points should be...
        # [x2,y2],[x2-30,y2+6],[x2-5,y2+22]
        pygame.draw.polygon(self.window,colorB, ([Maru_x+130,Maru_y],[Maru_x+99,Maru_y+6],[Maru_x+124,Maru_y+22]))  # right ear
        pygame.draw.polygon(self.window,colorB, ([Maru_x+40,Maru_y+68],[Maru_x+90,Maru_y+68],[Maru_x+65,Maru_y+20]))  # face triangle
        # left and right eyes (whites)
        pygame.draw.circle(self.window,self.white, (Maru_x+40,Maru_y+40),15)
        pygame.draw.circle(self.window,self.white, (Maru_x+90,Maru_y+40),15)
        # left and right eyes (blacks)
        pygame.draw.circle(self.window,self.black, (Maru_x+40,Maru_y+40),10)
        pygame.draw.circle(self.window,self.black, (Maru_x+90,Maru_y+40),10)

        pygame.draw.polygon(self.window,self.black,([Maru_x+60,Maru_y+40],[Maru_x+70,Maru_y+40],[Maru_x+65,Maru_y+45]))  # muzzle
        pygame.draw.arc(self.window,self.black,(Maru_x+52,Maru_y+35,15,15),4.7,6.3,2)  # left muzzle line
        pygame.draw.arc(self.window, self.black, (Maru_x + 65, Maru_y + 35, 15, 15), 3.14, 4.9,2)  # right muzzle line
        pygame.draw.polygon(self.window,(247,51,51),([Maru_x+60,Maru_y+49],[Maru_x+65,Maru_y+46],[Maru_x+70,Maru_y+49],[Maru_x+65,Maru_y+60]))  # mouth

        # left and right arms
        pygame.draw.line(self.window,self.white,(Maru_x+30,Maru_y+75),(Maru_x+10,Maru_y+120),3)
        pygame.draw.line(self.window,self.white,(Maru_x+99,Maru_y+75),(Maru_x+120,Maru_y+100),3) # right arm bend
        pygame.draw.line(self.window,self.white,(Maru_x+120,Maru_y+100),(Maru_x+140,Maru_y+75),3)

        # left and right hands
        pygame.draw.circle(self.window,colorB,(Maru_x+140,Maru_y+75),10)
        pygame.draw.circle(self.window,colorB,(Maru_x+10,Maru_y+120),10)

        # left and right legs
        pygame.draw.line(self.window,self.white,(Maru_x+50,Maru_y+170),(Maru_x+20,Maru_y+200),3)
        pygame.draw.line(self.window,self.white,(Maru_x+80,Maru_y+170),(Maru_x+110,Maru_y+200),3)

        # left and right feet
        pygame.draw.circle(self.window,colorB,(Maru_x+20,Maru_y+200),10)
        pygame.draw.circle(self.window,colorB,(Maru_x+110,Maru_y+200),10)


class User:  # User refers to the interface that displays user's input

    def __init__(self,window):

        self.font = pygame.font.SysFont('consolas', 25, True)
        self.window = window
        self.white = (255,255,255)
        self.xy = [self.window.get_width(),self.window.get_height()]
        self.black = (0,0,0)

    def draw(self):
        self.user_body()
        self.user_bubl()

    def user_body(self):

        pygame.draw.circle(self.window,self.white,(30,self.xy[1]),160) # user head
        # next 6 are user hair (right strand then left strand)
        pygame.draw.line(self.window,self.white,(30,self.xy[1]-160),(40,self.xy[1]-200),1)
        pygame.draw.arc(self.window,self.white,([20,self.xy[1]-215],[20,30]),6.3,3.14)
        pygame.draw.arc(self.window,self.white,(20,self.xy[1]-213,10,15),3.14,6.3)
        pygame.draw.line(self.window,self.white,(20,self.xy[1]-160),(19,self.xy[1]-200),1)
        pygame.draw.arc(self.window,self.white,([0,self.xy[1]-215],[20,30]),6.3,3.14)
        pygame.draw.arc(self.window,self.white,(0,self.xy[1]-213,10,15),3.14,6.3)
        # user eye white and black aka filled black circle inside unfilled black circle
        pygame.draw.circle(self.window,self.black,(150,self.xy[1]-90),30)
        pygame.draw.circle(self.window, self.black, (150, self.xy[1] - 90), 20)

    def user_bubl(self):
        coords = [[(200,self.xy[1]-40),(250,self.xy[1]-110)],[(250,self.xy[1]-110),(self.xy[0],self.xy[1]-110)],
                  [(self.xy[0]-3,self.xy[1]-110),(self.xy[0]-3,self.xy[1])],[(self.xy[0]-3,self.xy[1]-3),(250,self.xy[1]-3)],
                  [(250,self.xy[1]-3),(250,self.xy[1]-60)],[(250,self.xy[1]-60),(200,self.xy[1]-41)]]
        for i in range(len(coords)):  # draw the dialogue bubble for user
            pygame.draw.line(self.window,self.white,coords[i][0],coords[i][1],5)

    def user_input(self,inpt,turn,dialogue):

        # pre-determines how user should answer
        preset = ["My name is: ",
                  'My day has been ',
                  'Because ',
                  '(say bye): ',
                  '1. Sure, why not?          '
                  '2. Sorry, gotta go!        '
                  '(Press 1 or 2)',
                  '' ]

        text = ''

        if dialogue == 0:  # before selecting tips
            text = preset[turn]+inpt
        elif dialogue > 0:  # when looking at tips, show blank on user bubble
            text = ''

        txt_w = len(text)  # width of text counted in # of characters
        txt_h = self.font.get_height()  # height counted in pixels
        lines = math.ceil(txt_w / 27)  # rounded up; number of lines needed for displaying text
        texts = [text[i:i + 27] for i in range(0, txt_w, 27)]  # list of texts, split every 25 characters

        for each_line in range(lines):  # displays each line of text

            text = self.font.render(texts[each_line], True, self.white)  # renders each line

            txt_x = 254  # co-ordinate for beginning of text
            txt_y = self.xy[1]-106 + txt_h * each_line

            textRect = text.get_rect()
            textRect.center = (txt_x, txt_y)  # y co-ordinate adjusted according to number of lines
            self.window.blit(text, (txt_x, txt_y))


main()
