#pragma once
#include<iostream>

using namespace std;

template<class T>
class MyArray {
    public:
    MyArray(int capacity){
        cout << "Creator func" << endl;
        this->capacity = capacity;
        this->size = 0;
        this->pAddress = new T[this->capacity];
    }
    MyArray(const MyArray &arr){
        cout << "Copy creator func" << endl;
        this->capacity = arr.capacity;
        this->size = arr.size;
        this->pAddress = new T[arr.capacity];
        for(int i=0; i<arr.size; i++){
            this->pAddress[i] = arr.pAddress[i];
        }
    }

    ~MyArray(){
        cout << "Desructuor func" << endl;
        // cout <<
        if (this->pAddress != NULL){
            delete[] this->pAddress;
            this->pAddress = NULL;
            this->capacity = 0;
            this->size = 0;
        }
    }

    MyArray & operator=(const MyArray & arr) {
        cout << "operator=" << endl;
        if(this->pAddress != NULL){
            delete[] this->pAddress;
            this->capacity = 0;
            this->size = 0;
        }
        this->capacity = arr.capacity;
        this->size = arr.size;
        this->pAddress = new T[this->capacity];
        for(int i=0; i<this->size; i++){
            this->pAddress[i] = arr.pAddress[i];
        }
        return *this;
    }

    T& operator[](int i){
        return this->pAddress[i];

    }

    void push_back(const T &item){
        if (this->size == this->capacity){
            return;
        }
        this->pAddress[this->size] = item;
        this->size ++;
    }

    void pop_back(){
        if(this->size==0){
            return;
        }
        this->size--;
    }

    int get_capacity(){
        return this->capacity;
    }
    int get_size() {
        return this->size;
    }


    private:
    int capacity;
    int size;
    T* pAddress;
};