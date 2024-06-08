import React, { useState } from "react";
import styled from "styled-components";
import { Link, useNavigate } from "react-router-dom";
import {
  DropDownContainer,
  DropDownListContainer,
  DropDownList,
  ListItem,
} from "../components/NavBar";
import { KeyboardArrowDownOutlined } from "@material-ui/icons";

const Container = styled.div`
  width: 100%;
  margin-left: 6px;
`;

export const Brand = styled.div`
  display: flex;
  width: 100%;

  justify-content: flex-start;
  align-items: center;
  cursor: pointer;
`;

export const BrandName = styled.h1`
  color: #00308f;
  font-weight: bold;
  align-items: center;
  justify-content: center;
`;

export const BrandLogo = styled.div`
  align-items: center;
  justify-content: center;
`;

const SideBar = () => {
  const [toggle, setToggle] = useState(false);

  const navigate = useNavigate();

  const brandClick = () => {
    navigate("/");
  };
  const handleDropDown = () => {
    setToggle(!toggle);
  };

  const CustomerMenu = () => (
    <div>
      <Link className="nav-link mb-4 sidebar-link" to="/">
        <span>
          <img src="/static/icons/users.PNG" alt="userslogo" />
        </span>
        Users
      </Link>

      <Link className="nav-link mb-4 sidebar-link" to="/">
        <span>
          <img src="/static/icons/guarantor.PNG" alt="guarantorlogo" />
        </span>
        Guarantors
      </Link>

      <Link className="nav-link mb-4 sidebar-link" to="/">
        <span>
          <img src="/static/icons/loan.PNG" alt="loanlogo" />
        </span>
        Loans
      </Link>

      <Link className="nav-link mb-4 sidebar-link" to="/">
        <span>
          <img src="/static/icons/decision_model.PNG" alt="decisionlogo" />
        </span>
        Decision Models
      </Link>

      <Link className="nav-link mb-4 sidebar-link" to="/">
        <span>
          <img src="/static/icons/savings.PNG" alt="savingslogo" />
        </span>
        Savings
      </Link>

      <Link className="nav-link mb-4 sidebar-link" to="/">
        <span>
          <img src="/static/icons/loan_request.PNG" alt="loanRequestlogo" />
        </span>
        Loan Requests
      </Link>

      <Link className="nav-link mb-4 sidebar-link" to="/">
        <span>
          <img src="/static/icons/karma.PNG" alt="karmalogo" />
        </span>
        Karma
      </Link>
    </div>
  );

  const BusinessMenu = () => (
    <div>
      <Link className="nav-link mb-4 sidebar-link" to="/">
        <span>
          <img src="/static/icons/org.PNG" alt="orglogo" />
        </span>
        Organization
      </Link>

      <Link className="nav-link mb-4 sidebar-link" to="/">
        <span>
          <img src="/static/icons/loan_product.PNG" alt="logo" />
        </span>
        Loan Products
      </Link>

      <Link className="nav-link mb-4 sidebar-link" to="/">
        <span>
          <img src="/static/icons/saving_product.PNG" alt="logo" />
        </span>
        Savings Products
      </Link>

      <Link className="nav-link mb-4 sidebar-link" to="/">
        <span>
          <img src="/static/icons/fees_charges.PNG" alt="logo" />
        </span>
        Fees and Charges
      </Link>

      <Link className="nav-link mb-4 sidebar-link" to="/">
        <span>
          <img src="/static/icons/transactions.PNG" alt="logo" />
        </span>
        Transactions
      </Link>

      <Link className="nav-link mb-4 sidebar-link" to="/">
        <span>
          <img src="/static/icons/services.PNG" alt="logo" />
        </span>
        Services
      </Link>

      <Link className="nav-link mb-4 sidebar-link" to="/">
        <span>
          <img src="/static/icons/service_account.PNG" alt="logo" />
        </span>
        Service Account
      </Link>

      <Link className="nav-link mb-4 sidebar-link" to="/">
        <span>
          <img src="/static/icons/settlement.PNG" alt="logo" />
        </span>
        Settlements
      </Link>

      <Link className="nav-link mb-4 sidebar-link" to="/add-profile">
        <span>
          <img src="/static/icons/reports.PNG" alt="logo" />
        </span>
        Reports
      </Link>
    </div>
  );

  const settingMenu = () => (
    <div>
      <Link className="nav-link mb-4 sidebar-link" to="/">
        <span>
          <img src="/static/icons/preferences.PNG" alt="logo" />
        </span>
        Preferences
      </Link>
      <Link className="nav-link mb-4 sidebar-link" to="/">
        <span>
          <img src="/static/icons/fees_pricing.PNG" alt="logo" />
        </span>
        Fees and Pricing
      </Link>
      <Link className="nav-link mb-4 sidebar-link" to="/">
        <span>
          <img src="/static/icons/audit_log.PNG" alt="logo" />
        </span>
        Audit Logs
      </Link>
    </div>
  );

  return (
    <Container>
      <Brand
        onClick={() => {
          brandClick();
        }}
      >
        <BrandLogo>
          <img
            src="/static/icons/brandlogo.jpg"
            style={{ height: 50, width: 50 }}
            alt="brandlogo"
          />
        </BrandLogo>
        <BrandName>boomer</BrandName>
      </Brand>
      <div className="sidebar-link sw">
        <span>
          <img src="/static/icons/dashboard.PNG" alt="dash" />
        </span>{" "}
        Switch Organization{" "}
        <span>
          {" "}
          <KeyboardArrowDownOutlined
            style={{ cursor: "pointer" }}
            onClick={handleDropDown}
          />{" "}
        </span>{" "}
      </div>
      <DropDownContainer style={{ paddingBottom: "15px", paddingLeft: "0px" }}>
        <DropDownListContainer>
          <DropDownList className={toggle ? "show-dropdown" : "hide-dropdown"}>
            <ListItem>lendsqr</ListItem>
            <ListItem>irorun</ListItem>
            <ListItem>awale</ListItem>
          </DropDownList>
        </DropDownListContainer>
      </DropDownContainer>
      <div
        className="sidebar-link"
        style={{ marginBottom: "30px", display: "flex" }}
      >
        <img src="/static/icons/dash.PNG" alt="dash" />

        <Link className="nav-link sidebar-link" to="/add-profile">
          Add Profile
        </Link>
      </div>
      <div className="sidebar-title mb-3">CUSTOMERS</div>
      {CustomerMenu()}
      <div className="sidebar-title mb-3">BUSINESSES</div>
      {BusinessMenu()}
      <div className="sidebar-title mb-3">SETTINGS</div>
      {settingMenu()}
    </Container>
  );
};

export default SideBar;
