#include<iostream>
using namespace std;

class CPU {
    public:
    virtual void calculate() = 0;
    virtual ~CPU(){};
};

class GPU{
    public:
    virtual void display() = 0;
    virtual ~GPU(){};
};

class Memory{
    public:
    virtual void storage() = 0;
    virtual ~Memory(){};
};

class Computer{
    public:
    Computer(CPU* cpu, GPU* gpu, Memory* memory){
        m_cpu = cpu;
        m_gpu = gpu;
        m_memory = memory;
    }

    void work(){
        m_cpu->calculate();
        m_gpu->display();
        m_memory->storage();
    }

    ~Computer(){
        if(m_cpu!=NULL){
            //如果没有 virtual ~CPU(){};
            //会有警告 warning: delete called on 'CPU' that is abstract but has non-virtual destructor
            //但因为虚类的子类没有在堆区申请内存所以是安全的

            delete m_cpu;
            m_cpu = NULL;
            cout << "Deleted CPU." << endl;
        }
        if(m_gpu!=NULL){
            delete m_gpu;
            m_gpu = NULL;
            cout << "Deleted GPU." << endl;
        }
        if(m_memory!=NULL){
            delete m_memory;
            m_memory = NULL;
            cout << "Deleted memory." << endl;
        }
    }

    private:
    CPU * m_cpu;
    GPU * m_gpu;
    Memory * m_memory;
};


// 厂商
class IntelCPU: public CPU{
    public:
    virtual void calculate(){
        cout << "Intel CPU is calculating...\n";
    }
};
class IntelGPU: public GPU{
    public:
    void display(){
        cout << "Intel GPU is displaying...\n";
    }
};
class IntelMemory: public Memory{
    public:
    void storage(){
        cout << "Intel memory is storing...\n";
    }
};

int main() {
    CPU * intelcpu = new IntelCPU;
    GPU * intelgpu = new IntelGPU;
    Memory * intelmomory = new IntelMemory;
    
    Computer * computer = new Computer(intelcpu, intelgpu, intelmomory);
    computer->work();
    delete computer;
}