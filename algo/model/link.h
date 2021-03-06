#ifndef LINK
#define LINK

#include "defs.h"
#include "virtualLink.h"
#include "netelement.h"
#include "routing.h"

class Link {
public:
	Link(Port* port1, Port* port2, long capacity = 12500, float length2 = 1.0):
		port1(port1),
		port2(port2),
		maxCapacity(capacity),
		freeCapacityFromPort1(capacity),
		freeCapacityFromPort2(capacity),
        length(length2),
        countLinks(0) {
	}

	inline Port* getPort1() const {
		return port1;
	}

	inline Port* getPort2() const {
		return port2;
	}

	inline Port* getPortByParent(NetElement* elem) {
	    if ( port1->getParent() == elem )
	        return port1;
	    if ( port2->getParent() == elem )
	        return port2;
	    return 0;
	}

	inline NetElement* getElementByPort(Port* port) {
	    if ( port1 == port )
	        return port1->getParent();
	    if ( port2 == port )
            return port2->getParent();
	}

    inline long getCountLinks() const {
        return countLinks;
    }

    inline float getLength() const {
        return length;
    }

	inline long getMaxCapacity() const {
		return maxCapacity;
	}

	inline long getFreeCapacityFromPort1() const {
		return freeCapacityFromPort1;
	}

	inline long getFreeCapacityFromPort2() const {
		return freeCapacityFromPort2;
	}

	inline long getFreeCapacityFromPort(Port* port) const {
	    if ( port == port1 )
	        return freeCapacityFromPort1;
	    return freeCapacityFromPort2;
	}

	inline bool isAssignmentPossible(float bandwidth, Port* fromPort) {
        if ( port1 == fromPort && freeCapacityFromPort1 >= bandwidth )
            return true;

        if ( port2 == fromPort && freeCapacityFromPort2 >= bandwidth )
            return true;
    }

	bool isAssignmentPossible(VirtualLink* virtualLink, Port* fromPort) {
	    return isAssignmentPossible(virtualLink->getBandwidth(), fromPort);
	}

	 bool assignVirtualLinks(VirtualLink* virtualLink, Port* fromPort, bool highPriority = false) {
	    if ( isAssigned (virtualLink) )
	        return true;

	    if ( !isAssignmentPossible(virtualLink, fromPort) )
	        return false;

	    if ( port1 == fromPort ) {
	        freeCapacityFromPort1 -= virtualLink->getBandwidth(); // +1 required to normalize correctly
	        assignedFromPort1.insert(virtualLink);
	    } else {
	        freeCapacityFromPort2 -= virtualLink->getBandwidth();
	        assignedFromPort2.insert(virtualLink);
	    }
	    fromPort->getParent()->assignOutgoingVirtualLink(virtualLink, fromPort, highPriority);
        if (!countLinks) {
            SumLen += length;
        }
        countLinks += 1;
	    return true;
	}

	inline void removeVirtualLink(VirtualLink* virtualLink) {
	    Port* port = 0;
        bool flag = false;
	    if ( assignedFromPort1.find(virtualLink) != assignedFromPort1.end() ) {
	        assignedFromPort1.erase(virtualLink);
	        freeCapacityFromPort1 += virtualLink->getBandwidth();
	        port = port1;
            flag = true;
	    }

	    if ( assignedFromPort2.find(virtualLink) != assignedFromPort2.end() ) {
            assignedFromPort2.erase(virtualLink);
            freeCapacityFromPort2 += virtualLink->getBandwidth();
            port = port2;
            flag = true;
        }

        if (flag) {
            countLinks -= 1;
            if (!countLinks) {
                SumLen -= length;
            }
        }
	    if ( port != 0 )
	        port->getParent()->removeOutgoingVirtualLink(virtualLink, port);
	}

	inline bool isAssigned(VirtualLink* vl) {
	    return assignedFromPort1.find(vl) != assignedFromPort1.end()
	            || assignedFromPort2.find(vl) != assignedFromPort2.end();
	}

	inline VirtualLinks& getAssignedFromPort(Port* port) {
	    assert(port == port1 || port == port2);
	    if ( port == port1 )
	        return assignedFromPort1;
	    return assignedFromPort2;
	}

private:
	Port* port1;
	Port* port2;
	long maxCapacity;
	long freeCapacityFromPort1;
	long freeCapacityFromPort2;
    float length;
    long countLinks;

	VirtualLinks assignedFromPort1;
	VirtualLinks assignedFromPort2;
};


#endif
