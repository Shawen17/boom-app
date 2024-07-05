import React, { useState, useContext } from "react";
import { Table } from "reactstrap";
import { MoreVertOutlined, FilterListOutlined } from "@material-ui/icons";
import { useNavigate } from "react-router-dom";
import FilterForm from "./FilterForm";
import { PageButton, Pagination as Paginate } from "./Styled";
import ArrowBackIosIcon from "@mui/icons-material/ArrowBackIos";
import ArrowForwardIosIcon from "@mui/icons-material/ArrowForwardIos";
import { StatusUpdate } from "./utility/AdminAction";
import axios from "axios";
import { UserContext } from "./ContextManager";
import { PageInput } from "./authenticationStyles/StyledAuth";

const Users = (props) => {
  const PageSize = props.PageSize;
  const [menu, setMenu] = useState();
  const [submenu, setSubmenu] = useState(false);
  const [clicked, setClicked] = useState(false);
  const [inputs, setInputs] = useState({});
  const [filtered, setFiltered] = useState(0);
  const [position, setPosition] = useState({ top: 0, left: 0 });
  const navigate = useNavigate();
  const result = useContext(UserContext);

  const handleChange = (event) => {
    const name = event.target.name;
    const value = event.target.value;
    setInputs((values) => ({ ...values, [name]: value }));
    props.handleChange((values) => ({ ...values, [name]: value }));
  };

  const onFilter = () => {
    setFiltered(filtered + 1);
    props.onFilter(filtered + 1);
  };

  const onReset = () => {
    setInputs({});
    setFiltered(0);
    props.onReset();
  };

  const filterClick = (event) => {
    setPosition({ top: event.pageY + 20, left: event.pageX - 30 });
    setClicked(!clicked);
    props.filterClick();

    if (clicked) {
      onReset();
    }
  };

  const displayDetails = (person, path) => {
    setMenu();
    navigate(path, { state: person });
  };

  const blacklistUser = (id) => {
    StatusUpdate(axios, "blacklist", id);
    props.updateStatus();
  };

  const activateUser = (id) => {
    StatusUpdate(axios, "activate", id);
    props.updateStatus();
  };

  const displayMenu = (index) => {
    setMenu(index);
  };

  const customStatus = (status) => {
    if (status === "Active") {
      return <span id="active-status">Active</span>;
    } else if (status === "Inactive") {
      return <span id="inactive-status">Inactive</span>;
    } else if (status === "Pending") {
      return <span id="pending-status">Pending</span>;
    } else if (status === "Blacklisted") {
      return <span id="blacklisted-status">Blacklisted</span>;
    }
  };

  const formatDate = (str) => {
    let date = new Date(str);
    return date.toDateString();
  };

  return (
    <div style={{ borderRadius: "6px", backgroundColor: "white" }}>
      {clicked && (
        <FilterForm
          handleChange={handleChange}
          onFilter={onFilter}
          onReset={onReset}
          inputs={inputs}
          style={position}
        />
      )}

      <Table borderless style={{ position: "relative", maxWidth: "100vw" }}>
        <thead>
          <tr>
            <th onClick={filterClick}>
              ORGANIZATION <FilterListOutlined />{" "}
            </th>
            <th onClick={filterClick}>
              USERNAME <FilterListOutlined />
            </th>
            <th onClick={filterClick}>
              EMAIL <FilterListOutlined />
            </th>
            <th onClick={filterClick}>
              PHONE NUMBER <FilterListOutlined />
            </th>
            <th onClick={filterClick}>
              DATE JOINED <FilterListOutlined />
            </th>
            <th onClick={filterClick}>
              STATUS <FilterListOutlined />
            </th>
            <th></th>
          </tr>
        </thead>

        <tbody>
          {result.users_paginated.map((user, index) => {
            return (
              <tr
                key={index}
                style={{
                  borderBottom: "1px solid #ccc",
                  height: "60px",
                  opacity: 1,
                  justifyContent: "center",
                }}
              >
                <td
                  className="nav-link sidebar-link"
                  style={{ cursor: "pointer" }}
                  onClick={() => displayDetails(user, "/update-profile")}
                >
                  {user.organization.orgName}
                </td>
                <td>{user.profile.userName}</td>
                <td>{user.profile.email}</td>
                <td>{user.profile.phoneNumber}</td>
                <td>{formatDate(user.createdAt)}</td>
                <td>{customStatus(user.profile.status)}</td>
                <td>
                  <button
                    onClick={() => {
                      displayMenu(index);
                      setSubmenu(!submenu);
                    }}
                    style={{ border: "none", backgroundColor: "white" }}
                  >
                    <MoreVertOutlined className="menu-bar" />
                    <ul
                      className={
                        menu === index && submenu
                          ? "show-menu-options"
                          : "hide-menu-options"
                      }
                    >
                      <li
                        onClick={() => {
                          displayDetails(user, "/user-details");
                        }}
                      >
                        View Details
                      </li>
                      <li
                        onClick={() => {
                          blacklistUser(user._id);
                        }}
                      >
                        Blacklist
                      </li>
                      <li
                        onClick={() => {
                          activateUser(user._id);
                        }}
                      >
                        Activate
                      </li>
                    </ul>
                  </button>
                </td>
              </tr>
            );
          })}
        </tbody>
      </Table>
      <Paginate>
        <PageButton onClick={() => props.prevPage()}>
          <ArrowBackIosIcon />
        </PageButton>
        <PageButton onClick={() => props.nextPage()}>
          <ArrowForwardIosIcon />
        </PageButton>
        <div>
          {props.page} of {Math.ceil(result.all_users / PageSize)}...
        </div>
        per page{" "}
        <PageInput
          type="number"
          name="itemCount"
          value={inputs.itemCount || ""}
          onChange={handleChange}
        />
      </Paginate>
    </div>
  );
};

export default React.memo(Users);
