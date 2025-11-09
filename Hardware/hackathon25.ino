#include "Rotary_Encoder.h"
#include "UI.h"
#include "nrf.h"

const char *Roll = "ROLL"; 
const char* GO_COMMAND = "go";
int current_prop = 0; // index of currently shown property (global)

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

void addProperty(String name, int rent = 0) {
    if (prop_size < 30) {
        all_props[prop_size].name = name;
        all_props[prop_size].Rent = rent;
        prop_size++;
        current_prop = prop_size - 1; // show the newly added property immediately
    }
}

void loop() {
    String landed = recieve_landing();

    // Trigger Buy/Skip menu if a property is landed
    if (landed != "none" && !waiting_for_buy) {
        waiting_for_buy = true;
        mode = FINAL;
        menu = OUTSIDE_OPT;
        options = 0;
        roll_clicked = false;
        updateScreen("Buy or Skip");
    }

    // If roll finished but no property landed
    if (landed == "none" && mode == WAIT) {
        mode = START;
        menu = OUTSIDE_OPT;
        roll_clicked = true;
        general_menu();
    }

    // Start menu flow
    if (Start_menu != 2){
        game_start();
        return; // skip rest of loop until start menu done
    }

    // Handle "go" command
    if (recieve_and_go()){
        setStateTurn();
    }

    // OUTSIDE_OPT menu
    if (menu == OUTSIDE_OPT){
        general_menu();
        if (click()){
            menu = INSIDE_OPT;
            enter_option();
        }
    }

    // INSIDE_OPT menu
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

    // FINAL mode: Buy/Skip
    if (mode == FINAL && waiting_for_buy) {
        general_menu(); // always displays Buy/Skip

        if (click()) {
            if (options == 0) { // Buy
                updateScreen("Bought!");
                addProperty(landed);
                send("BUY");
                delay(800);
            } 
            else if (options == 1) { // Skip
                updateScreen("Skipped!");
                send("SKIP");
                delay(800);
            }

            // ✅ End of Buy/Skip action
            updateScreen("Turn done!");
            delay(800);
            waiting_for_buy = false;
            mode = PTURN;          // back to player’s turn menu
            menu = OUTSIDE_OPT;    // ready to pick options again
            roll_clicked = true;
            general_menu();
        }
    }
}

// --- Helper Functions ---

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

void viewProp() {
    if (prop_size == 0) {
        updateScreen("none");
        current_prop = 0;
    } else {
        int move = turn(); // use rotary to browse
        if (move != 0) {
            current_prop = (current_prop + move) % prop_size;
            if (current_prop < 0) current_prop += prop_size;
        }
        updateScreen(all_props[current_prop].name);
    }
    display_property = true;
}

void general_menu() {
    if (mode == FINAL) {
        Final_Screen();  // always display Buy/Skip
        return;
    }
    if (update_options()) { 
        if (mode == START) Start_screen();
        else if (mode == PTURN) Pturn_screen();
        else if (mode == WAIT) updateScreen("");
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
