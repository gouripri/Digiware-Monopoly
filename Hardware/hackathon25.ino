#include "Rotary_Encoder.h"
#include "UI.h"
#include "nrf.h"

const char *Roll = "ROLL"; 
const char* GO_COMMAND = "go";

class Properties {       
public: 
    String name;                 
    int Rent;  
};

// FSM states
int mode = START; 
int Start_menu = 0;
int options = 0;
int balance = 1500;
int menu = 0;
bool display_balance = false;
bool roll_clicked = true; 
bool display_property = false;
bool waiting_for_buy = false;

Properties all_props[30] = {};
char names[5][10] = {"bull","tophat","dog","discord","python"};
int prop_size = 0;

void setup() {
    Serial.begin(9600);

    UI_setup();
    RotaryEncoder_setup();
    nrf_setup_reciever();
}

void loop() {
  String landed = recieve_landing();
  if (landed != "none" && !waiting_for_buy) {
      waiting_for_buy = true;
      mode = FINAL;
      menu = OUTSIDE_OPT;
      options = 0; // default to Buy
      updateScreen("Buy or Skip");
  }


    if(Start_menu != 2){
        game_start();
        return; // skip rest of loop until start menu done
    }

  
    if (recieve_and_go()){
        setStateTurn();
    }


    if (menu == OUTSIDE_OPT){
        general_menu();
        if (click()){
            menu = INSIDE_OPT;
            enter_option();
        }
    }

if (menu == INSIDE_OPT) {
     if (click() && display_balance) {
        menu = OUTSIDE_OPT;
        display_balance = false;
        general_menu();
    }

       if (click() && display_property) {
        menu = OUTSIDE_OPT;
        display_property = false;
        general_menu();
    }

     if (click() && roll_clicked && mode != FINAL) {
        menu = AFTER_ROLL;
        mode = WAIT;
        roll_clicked = false;
        general_menu();
    }
}


    


    if (mode == FINAL && waiting_for_buy) {
        general_menu();

        if (click()) {
            if (options == 0) { // Buy
                updateScreen("Bought!");
                send("BUY");
                delay(800);
            } 
            else if (options == 1) { // Skip
                updateScreen("Skipped!");
                send("SKIP");
                delay(800);
            }

            // Reset to START
            waiting_for_buy = false;
            mode = START;
            Start_menu = 0;
            menu = 0;
            roll_clicked = true;
            general_menu();
        }
    }

   // String landed = recieve_landing();
    if(landed != "none"){
        // Trigger FINAL state menu
        waiting_for_buy = true;
        mode = FINAL;
        menu = OUTSIDE_OPT;
        options = 0; // default to Buy
        updateScreen("Buy or Skip");
    }
}









void roll(){
    roll_clicked = true;
    send(Roll);
    nrf_setup_reciever();
}

void setStateTurn(){
    mode = PTURN;
    nrf_setup_transmitter();
}

void viewIcons(){}

void enter_option() {
    if (mode == START){
        if (options == 0){ 
            viewProp();
            menu = INSIDE_OPT; 
        }
        else if (options == 1){ 
            viewBalance();
            display_balance = true;
            menu = INSIDE_OPT; 
        }
        else if (options == 2) viewIcons();
    }
    else if (mode == PTURN){
        if (options == 0){ // Properties
            viewProp();
            menu = INSIDE_OPT; 
        }
        else if (options == 1){ // Balance
            viewBalance();
            display_balance = true;
            menu = INSIDE_OPT; 
        }
        else if (options == 2) roll();
    }
}


void viewBalance(){
    updateScreen(String(balance));
}

void viewProp(){
    if (prop_size == 0){
        updateScreen("none");
    } else {
        updateScreen(all_props[0].name); 
    }
    display_property = true;
}


void general_menu() {
    if (update_options() || mode == FINAL) { 
        if (mode == START) Start_screen();
        else if (mode == PTURN) Pturn_screen();
        else if (mode == WAIT) updateScreen("");
        else if (mode == FINAL) Final_Screen();
    }
}


int game_start(){
    if (Start_menu ==0){
        if (click()){
            Start_menu = 1;
            updateScreen("Player 1");  // CHANGE THIS FOR EACH REMOTE
        }
    }
    else if (Start_menu ==1){
        while (!click()){}
        Start_menu =2;
        updateScreen("Properties");
    }
    return 0;
}

bool update_options(){
    int adder = turn();
    bool change = false;

    if(adder != 0){
        if((adder == -1 && options > 0) ||
           (adder == 1 && (mode == PTURN || mode == START) && options < 2) ||
           (adder == 1 && (mode != PTURN && mode != START) && options < 1)) {
            options += adder;
            change = true;
        }
    }

    return change;
}
void update_choose_icon(){ }


void Start_screen(){
    if (options == 0) updateScreen("Properties");
    else if (options == 1) updateScreen("Balance");
    else if (options == 2) update_choose_icon();
}

void Pturn_screen(){
    if (options == 0) updateScreen("Properties");
    else if (options == 1) updateScreen("Balance");
    else if (options == 2) updateScreen("Roll");
}

void Final_Screen(){
    if(options == 0) updateScreen("Buy");
    else if (options == 1) updateScreen("Skip");
}
